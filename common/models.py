from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, unique=True)
    STOCK_FIRM_CHOICE = (
        ('키움증권', 'KIWOOM'),
        ('삼성증권', 'SAMSUNG'),
        ('한국투자증권', 'KOREA'),
        ('KB증권', 'KOOKMIN'),
        ('NH투자증권', 'NONGHYUP'),
        ('미래에셋증권', 'MIREA'),
        ('신한금융투자', 'SHINHAN'),
        ('그 외', 'ETC')
    )
    stock_firm = models.CharField(choices=STOCK_FIRM_CHOICE, max_length=10)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
