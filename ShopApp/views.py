from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError

from .models import User, Offer, Transaction

from django.utils import timezone
from datetime import timedelta


def getUser(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
        user = User.objects.filter(djangoUser=user)[0]
    else:
        raise Http404("Not valid user")
    return user


def getRedirectCode(url, params=dict()):
    code = ''
    code += '<head>'
    code += '<meta http-equiv="refresh" content="0; url={url}?{params}" />'.format(
        url=url,
        params='&'.join(k + '=' + v for k, v in params.items()),
    )
    code += '</head>'
    return code


class Index(View):
    '''
    This an is main page view.
    '''

    def get(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user

        template = loader.get_template('mainPageTemplate.html')
        context = {
            'loggedAs': user,
            'offersList': Offer.objects.all(),
            'usersList': User.objects.all(),
            'requestParams': ','.join(map(str, request.GET.items())),
            'requestCookies': '\n'.join(map(str, request.COOKIES.items())),
        }
        return HttpResponse(template.render(context, request))


class AccountPanel(View):
    '''
    Client view for managing account.
    '''

    def get(self, request):
        user = getUser(request)

        myOffersList = Offer.objects.filter(user=user)

        # TODO:
        myBuyTransactions = []
        mySellTransactions = []

        template = loader.get_template('accountPanel.html')
        context = {
            'loggedAs': user,
            'myOffersList': myOffersList,
            'myBuyTransactions': myBuyTransactions,
            'mySellTransactions': mySellTransactions,
        }
        return HttpResponse(template.render(context, request))


class OfferView(View):

    def get(self, request, offerId):
        try:
            offer = Offer.objects.get(pk=offerId)
        except Offer.DoesNotExist:
            raise Http404("Offer does not exist")

        user = None
        if request.user.is_authenticated:
            user = request.user

        offer = Offer.objects.get(id=offerId)
        template = loader.get_template('offerViewTemplate.html')
        context = {
            'loggedAs': user,
            'offer': offer,
        }
        return HttpResponse(template.render(context, request))


class LoginView(View):

    def get(self, request):
        # FIXME: do not sent raw password, use django utils for login dialog
        template = loader.get_template('loginView.html')

        invalidLogin = False
        if ('invalidLogin' in request.GET.keys()
                and request.GET['invalidLogin'] == 'true'):
            invalidLogin = True
        context = {
            'invalidLogin': invalidLogin,
        }
        return HttpResponse(template.render(context, request))


class LoginViewConfirm(View):

    def get(self, request):
        username = request.GET['login']
        password = request.GET['passwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            code = 'Logging in...'
            code += getRedirectCode('/')
            return HttpResponse(code)
        else:
            code = 'Wrong login'
            code += getRedirectCode('/login/', {'invalidLogin': 'true'})
            return HttpResponse(code)


class LogoutView(View):

    def get(self, request):
        logout(request)

        code = 'Logging out...'
        code += getRedirectCode('/')
        return HttpResponse(code)


class RegisterAccountView(View):

    def get(self, request):
        template = loader.get_template('registerUser.html')

        invalidData = False
        if ('invalidData' in request.GET.keys()
                and request.GET['invalidData'] == 'true'):
            invalidData = True
        context = {
            'invalidData': invalidData,
        }
        return HttpResponse(template.render(context, request))


class RegisterAccountViewConfirm(View):

    def get(self, request):

        password = request.GET['passwd']
        passwordConfirm = request.GET['passwdConfirm']
        if password != passwordConfirm:
            succeed = False
        else:
            try:
                succeed = True
                User.addUser(
                    username=request.GET['login'],
                    password=request.GET['passwd'],
                    name=request.GET['name'],
                    surname=request.GET['surname'],
                    email=request.GET['email'],
                )
            except IntegrityError:
                succeed = False

        if succeed:
            code = 'Creating user'
            code += getRedirectCode('/')
            return HttpResponse(code)
        else:
            code = 'Wrong data'
            code += getRedirectCode('/register/', {'invalidData': 'true'})
            return HttpResponse(code)


class CreateNewOfferView(View):

    def get(self, request):
        template = loader.get_template('createOfferForm.html')

        invalidData = False
        if ('invalidData' in request.GET.keys()
                and request.GET['invalidData'] == 'true'):
            invalidData = True
        context = {
            'invalidData': invalidData,
        }
        return HttpResponse(template.render(context, request))


class CreateNewOfferConfirm(View):

    def get(self, request):
        user = getUser(request)

        try:
            title = request.GET['title']
            description = request.GET['desc']
            price = int(request.GET['price'])
            availableItems = int(request.GET['count'])
            days = int(request.GET['days'])
            succeed = True
        except ValueError:
            succeed = False

        if succeed:
            Offer.objects.create(
                title=title,
                description=description,
                price=price,
                availableItems=availableItems,
                startDate=timezone.now(),
                endDate=timezone.now() + timedelta(days=days),
                user=user,
            )
            code = 'Creating offer'
            code = getRedirectCode('/account/')
            return HttpResponse(code)
        else:
            code = getRedirectCode('/createOffer/', {'invalidData': 'true'})
            return HttpResponse(code)
