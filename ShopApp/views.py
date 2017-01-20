from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from django.views import View

from .models import User, Offer, Offer


class Index(View):

    def get(self, request):
        # return super(Index, self).get(request, *args, **kwargs)
        # TODO: user authorization
        # from django.contrib.auth import authenticate, login
        # if request.user.is_anonymous():
        #     # Auto-login the User for Demonstration Purposes
        #     user = authenticate()
        #     login(request, user)

        template = loader.get_template('mainPageTemplate.html')
        context = {
            'offersList': Offer.objects.all(),
            'usersList': User.objects.all(),
            'requestParams': ','.join(map(str, request.GET.items())),
            'requestCookies': '\n'.join(map(str, request.COOKIES.items())),
        }

        return HttpResponse(template.render(context, request))


class OfferView(View):

    def get(self, request, offerId):
        offer = Offer.objects.get(id=offerId)
        template = loader.get_template('offerViewTemplate.html')
        context = {
            'offer': offer,
        }
        return HttpResponse(template.render(context, request))
