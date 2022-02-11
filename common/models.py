from django.conf import settings
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    USERNAME_FIELD = 'test'
    STOCK_FIRM_CHOICE = (
        ('KIWOOM', '키움증권'),
        ('SAMSUNG', '삼성증권'),
        ('KOREA', '한국투자증권'),
        ('KOOKMIN', 'KB증권'),
        ('NONGHYUP', 'NH투자증권'),
        ('MIREA', '미래에셋증권'),
        ('SHINHAN', '신한금융투자'),
        ('ETC', '그 외')
    )
    stock_firm = models.CharField(choices=STOCK_FIRM_CHOICE, max_length=10)


def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)


post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
