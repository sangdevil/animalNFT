import pycountry
import datetime
from django import forms

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Nation(models.Model):
    country_choices = [(country.alpha_2, country.name) for country in pycountry.countries]

    country_code = models.CharField(max_length=2, choices=country_choices, default="KR")
    
    def get_country_name(self):
        return pycountry.countries.lookup(self.country_code).name
    def formfield(self, **kwargs):
        kwargs['widget'] = forms.Select(choices=self.country_choices)
        return super().formfield(**kwargs)


class NftUser(AbstractUser):
    # id = models.AutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    # Custom fields and methods for the user
    user_image = models.ImageField(upload_to='images/user_images/%Y/%m/%d/', null=True, default='default_image.jpg')
    birth_date = models.DateField(null=True, default=datetime.date.today)
    password1 = models.CharField(max_length=20, default =1)
    password2 = models.CharField(max_length=20, default=1)
    # nation = models.CharField(max_length=2, choices=[], null=True)
    nation = models.CharField(max_length=3, null=True)
    NFT_wallet_addr = models.CharField(max_length=200, unique=True, null=True)
    NFT_private_key = models.CharField(max_length=200,  null=True)
    NFT_public_key = models.CharField(max_length=200,  null=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('nation').choices = self.get_country_choices()
        self._meta.get_field('nation').default = 'KR'

    def get_country_choices(self):
        import pycountry
        return [(country.alpha_2, country.name) for country in pycountry.countries]

    def __str__(self):
        return self.username

    # todo! user wallet
    
    
    
    
NftUser._meta.get_field('groups').remote_field.related_name = 'nftuser_groups'
NftUser._meta.get_field('user_permissions').remote_field.related_name = 'nftuser_user_permissions'