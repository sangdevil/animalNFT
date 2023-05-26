# Create your models here.
import pycountry
from django.db import models

from accounts.models import Nation, NftUser

# Create your models here.


class Category(models.Model):
    category_choices = (
    ('Dog', 'Dog'),
    ('Cat', 'Cat'),
    ('WithHuman', 'WithHuman'),
)
    name = models.CharField(max_length=50, choices=category_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'
        
        
class Nft_object(models.Model):
    title = models.CharField(max_length=255)
    nft_image = models.ImageField(upload_to='images/nft_images/%Y/%m/%d/')
    description = models.TextField(default='no')
    
    # todo!, nft = ?
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user가 owner 연결
    owner = models.ForeignKey(NftUser, on_delete=models.CASCADE)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
    def get_nation_img_url(self):
        return f'/blog/bootstrap/img/nations/{self.owner.nation.get_country_code()}.gif'
    
    def get_owner_img_url(self):
        return self.owner.user_image.url
    
    def get_nft_img_url(self):
        return self.nft_image.url
    
    def belongs_dog(self):
        return self.category.name == "Dog"
    
    def belongs_cat(self):
        return self.category.name == "Cat"
    
    def belongs_human(self):
        return self.category.name == "WithHuman"
    
