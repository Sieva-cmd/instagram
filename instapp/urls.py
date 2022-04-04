from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views
import instapp


urlpatterns =[

    path('',views.home,name ='home'),
    re_path(r'^search/', views.search_results, name='search_results'),
    # re_path(r'^image/(\d+)',views.article,name ='image')
    path('<int:image_id>/',views.image,name='image'),
    re_path(r'register/',views.register_request, name="register"),
    re_path(r'login/', views.login_request, name="login"),
    re_path(r'logout', views.logout_request, name= "logout"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)