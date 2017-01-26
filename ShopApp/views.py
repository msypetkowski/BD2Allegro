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
        user = getUser(request)

        template = loader.get_template('mainPageTemplate.html')
        context = {
            'loggedAs': user,
            'offersList': Offer.objects.all(),
            'usersList': User.objects.all(),
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
        myBuyTransactions = Transaction.objects.filter(user=user)
        mySellTransactions = Transaction.objects.filter(offer__user=user)

        template = loader.get_template('accountPanel.html')
        context = {
            'loggedAs': user,
            'myOffersList': myOffersList,
            'myBuyTransactions': myBuyTransactions,
            'mySellTransactions': mySellTransactions,
        }
        return HttpResponse(template.render(context, request))


class UserProfileView(View):

    def get(self, request, userId):
        try:
            user = User.objects.get(pk=userId)
        except User.DoesNotExist:
            raise Http404("User does not exist")

        user = getUser(request)

        displayedUser = User.objects.get(id=userId)

        offers = Offer.objects.filter(user=displayedUser)

        template = loader.get_template('userProfile.html')
        context = {
            'loggedAs': user,
            'user': displayedUser,
            'offers': offers,
        }
        return HttpResponse(template.render(context, request))


class OfferView(View):

    def get(self, request, offerId):
        try:
            offer = Offer.objects.get(pk=offerId)
        except Offer.DoesNotExist:
            raise Http404("Offer does not exist")

        user = getUser(request)

        invalidData = False
        if ('invalidData' in request.GET.keys()
                and request.GET['invalidData'] == 'true'):
            invalidData = True

        offer = Offer.objects.get(id=offerId)
        template = loader.get_template('offerViewTemplate.html')
        context = {
            'loggedAs': user,
            'offer': offer,
            'invalidData': invalidData,
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
        user = getUser(request)

        invalidData = False
        if ('invalidData' in request.GET.keys()
                and request.GET['invalidData'] == 'true'):
            invalidData = True
        context = {
            'invalidData': invalidData,
            'loggedAs': user,
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


class BuyOfferConfirm(View):

    def get(self, request):
        user = getUser(request)

        try:
            count = int(request.GET['count'])
            offerId = int(request.GET['offerId'])
            succeed = True
        except ValueError:
            succeed = False

        # FIXME: synchronization (mutex) and check if still possible

        if succeed:
            offer = Offer.objects.filter(id=offerId)[0]
            if count > offer.availableItems:
                succeed = False

        if succeed:
            newTransaction = Transaction.objects.create(
                user=user,
                offer=offer,
                numberOfItems=count,
                date=timezone.now(),
                paymentStatus=0,
            )
            newAvailableItems = offer.availableItems - count
            Offer.objects.filter(id=offerId).update(
                availableItems=newAvailableItems)
            code = 'Create Transaction'
            code = getRedirectCode('/transactions/' + str(newTransaction.id))
            return HttpResponse(code)
        else:
            code = getRedirectCode(
                '/offers/' + str(offerId), {'invalidData': 'true'})
            return HttpResponse(code)


class TransactionView(View):

    def get(self, request, transactionId):
        try:
            transaction = Transaction.objects.get(pk=transactionId)
        except Transaction.DoesNotExist:
            raise Http404("Transaction does not exist")

        user = getUser(request)

        template = loader.get_template('transactionViewTemplate.html')
        context = {
            'loggedAs': user,
            'transaction': transaction,
        }
        return HttpResponse(template.render(context, request))
