"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from ShopApp.views import Index, OfferView, LoginView, LoginViewConfirm, LogoutView, AccountPanel, UserProfileView
from ShopApp.views import RegisterAccountView, RegisterAccountViewConfirm
from ShopApp.views import CreateNewOfferView, CreateNewOfferConfirm, BuyOfferConfirm
from ShopApp.views import TransactionView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Index.as_view(), name='homePage'),
    url(r'^login/$', LoginView.as_view(), name='loginView'),
    url(r'^logout/$', LogoutView.as_view(), name='logoutView'),
    url(r'^loginConfirm/$', LoginViewConfirm.as_view(), name='loginViewConfirm'),
    url(r'^offers/(?P<offerId>[0-99999]+)/$',
        OfferView.as_view(), name='offerView'),
    url(r'^account/$', AccountPanel.as_view(), name='accountView'),
    url(r'^register/$', RegisterAccountView.as_view(), name='registerAccountView'),
    url(r'^registerConfirm/$', RegisterAccountViewConfirm.as_view(),
        name='registerAccountViewConfirm'),
    url(r'^createOffer/$', CreateNewOfferView.as_view(), name='createOfferView'),
    url(r'^createOfferConfirm/$', CreateNewOfferConfirm.as_view(),
        name='createOfferConfirm'),
    url(r'^buyOfferConfirm/$', BuyOfferConfirm.as_view(),
        name='buyOfferConfirm'),
    url(r'^transactions/(?P<transactionId>[0-99999]+)/$',
        TransactionView.as_view(), name='transactionView'),
    url(r'^users/(?P<userId>[0-99999]+)/$',
        UserProfileView.as_view(), name='userProfileView'),
]
