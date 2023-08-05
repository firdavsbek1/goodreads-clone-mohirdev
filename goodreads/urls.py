from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import path,include

from books.models import Review


def home_page(request):
    return render(request,'home.html')


def home_review_page(request):
    reviews=Review.objects.all().order_by('-created_at')
    page_size=request.GET.get('page_size',5)
    paginator=Paginator(reviews,page_size)
    page_number=request.GET.get('page',1)
    page_obj=paginator.get_page(page_number)
    return render(request,'home_page.html',context={'reviews':reviews,'page_obj':page_obj,'page_size':page_size})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path('books/',include('books.urls')),
    path('api/',include('api.urls')),
    path('api/auth/',include('rest_framework.urls')),

    path("",home_page,name='home'),
    path("home/",home_review_page,name='home_page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)