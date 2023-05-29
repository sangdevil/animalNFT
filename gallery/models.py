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
    like_users = models.ManyToManyField(NftUser, related_name='liked_nft_objects')

    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user가 owner 연결
    owner = models.ForeignKey(NftUser, on_delete=models.CASCADE)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tx_hash = models.CharField(max_length=255, null=True)
    token_URI = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.title
    
    # url은 homepage/gallery <- 이건 현재 폴더임 으로 요청이 가므로, 이를 염두해 둘 것.
    def get_nation_img_url(self):

        return f'/static/blog/bootstrap/img/nations/{self.owner.nation}.gif'
    
    @property
    def total_likes(self):
        return self.likes.count()

    def user_has_liked(self, user):
        return self.likes.filter(user=user).exists()
    
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
    
class Like(models.Model):
    user = models.ForeignKey(NftUser, on_delete=models.CASCADE)
    nft_object = models.ForeignKey(Nft_object, on_delete=models.CASCADE)