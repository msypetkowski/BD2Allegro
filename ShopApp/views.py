from django.shortcuts import render
from django.http import HttpResponse


from django.views import View

from .models import User, Offer, Transaction


class Index(View):

    def get(self, request, *args, **kwargs):
        # return super(Index, self).get(request, *args, **kwargs)
        # TODO: user authorization
        # from django.contrib.auth import authenticate, login
        # if request.user.is_anonymous():
        #     # Auto-login the User for Demonstration Purposes
        #     user = authenticate()
        #     login(request, user)

        code = ''
        code += '<h1>'
        code += "Internet shop home page (TODO)\n"
        code += '</h1>'

        code += '<h3>'
        code += 'Debug info:'
        code += '</h3>'

        code += '<br>'
        code += 'Given {0} args: {1}'.format(len(args), str(args))
        code += '<br>'
        code += 'Given {0} kwargs: {1} '.format(len(kwargs), str(kwargs))
        code += '<br>'
        code += 'Request params: ' + ','.join(map(str, request.GET.items()))
        code += '<br>'
        code += 'Request cookies: ' + ','.join(map(str, request.COOKIES))
        code += '<br>'
        code += '<br>'

        code += '<h3>'
        code += 'List of registered users logins:'
        code += '</h3>'
        users = User.objects.all()
        code += ' '.join([u.login for u in users])

        code += '<h3>'
        code += 'List of transactions:'
        code += '</h3>'
        tr = Transaction.objects.all()
        code += ' '.join(map(str, tr))

        return HttpResponse(code)
