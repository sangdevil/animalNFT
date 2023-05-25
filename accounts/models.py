import pycountry
from django.db import models
# from gallery.models import Nft_object
from django.contrib.auth.models import AbstractUser


class Nation(models.Model):
    country_choices = [(country.name, country.alpha_2) for country in pycountry.countries]

    country_name = models.CharField(max_length = 50, choices=country_choices)
    
    def get_country_code(self):
        return pycountry.countries.lookup(self.country_name)


# class NftUser(AbstractUser):
    
#     # Custom fields and methods for the user
#     user_image = models.ImageField(upload_to='images/user_images/%Y/%m/%d/')
#     birth_date = models.DateField()
#     nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.username
#     # todo! user wallet