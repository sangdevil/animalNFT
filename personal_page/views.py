from django.shortcuts import render
from django.views.generic import ListView
from gallery.models import Nft_object
from django.db.models import Count
# Create your views here.

def home(request):
    return render(
        request,
        'single_pages/index.html',
    )
    
class HotFeed(ListView):
    model = Nft_object
    ordering = '-pk'
    context_object_name = "new_object_list"    
    template_name = 'single_pages/index.html'
    def get_queryset(self): # 컨텍스트 오버라이딩
      return Nft_object.objects.annotate(like_count = Count("like_users")).order_by('-like_count')[:2]
    
