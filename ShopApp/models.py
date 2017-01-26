from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    djangoUser = models.OneToOneField(DjangoUser)
    status = models.IntegerField(default=1)

    def __str__(self):
        # return 'User(login:{}, email:{})'.format(
        #     self.djangoUser.username,
        #     self.djangoUser.email,
        # )
        return self.djangoUser.username

    @classmethod
    def addUser(cls, username, password, name, surname, email):
        djangoUser = DjangoUser.objects.create_user(
            username=username,
            password=password,
            first_name=name,
            last_name=surname,
            email=email,
        )

        cls.objects.create(
            djangoUser=djangoUser,
            status=1,
        )


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    availableItems = models.IntegerField('available_items')
    startDate = models.DateTimeField('start_date')
    endDate = models.DateTimeField('end_date')

    def __str__(self):
        #return 'Offer(' + self.user.djangoUser.username + ':' + self.title + ')'
        return '{} : {}'.format(self.title, self.user)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    numberOfItems = models.IntegerField('number_of_items', default=1)
    date = models.DateTimeField()
    paymentStatus = models.IntegerField('payment_status')

    def __str__(self):
        return ('Transaction(buyer={},seller={},title={},date={})'.format(
                self.user.djangoUser.username,
                self.offer.user.djangoUser.username,
                self.offer.title,
                self.date))

# TODO: write other classes
