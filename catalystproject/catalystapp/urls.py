from django import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from django.conf import settings
from django.conf.urls.static import static


from . import views





urlpatterns = [
    # Admin Service 
    path('',views.uploadData),
    path('queryBuilder',views.queryBuilder),
    path('users',views.users),
    path('addUser',views.addUser),
    path('uploadCSVFile',views.uploadCSVFile),
    path('queryDateFilter',views.queryDateFilter),

    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)