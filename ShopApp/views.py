from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from django.views import View
from .models import User, Offer, Offer
from django.contrib.auth import authenticate, login, logout


class Index(View):
    '''
    This an is main page view.
    '''

    def get(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user

        # FIXME: mabe database query not iteration?
        myOffersList = [o for o in Offer.objects.all()
                        if o.user.djangoUser == user]

        template = loader.get_template('mainPageTemplate.html')
        context = {
            'loggedAs': user,
            'offersList': Offer.objects.all(),
            'myOffersList': myOffersList,
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
        user = None
        if request.user.is_authenticated:
            user = request.user
        else:
            raise Http404("Not valid user")

        # FIXME: mabe database query not iteration?
        myOffersList = [o for o in Offer.objects.all()
                        if o.user.djangoUser == user]

        template = loader.get_template('accountPanel.html')
        context = {
            'loggedAs': user,
            'myOffersList': myOffersList,
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
            code += '<head>'
            code += '<meta http-equiv="refresh" content="0; url=/" />'
            code += '/<head>'
            return HttpResponse(code)
        else:
            code = 'Wrong login'
            code += '<meta http-equiv="refresh" content="0; url=/login/?invalidLogin=true" />'
            return HttpResponse(code)


class LogoutView(View):

    def get(self, request):
        logout(request)

        code = 'Logging out...'
        code += '<head>'
        code += '<meta http-equiv="refresh" content="0; url=/" />'
        code += '/<head>'
        return HttpResponse(code)
