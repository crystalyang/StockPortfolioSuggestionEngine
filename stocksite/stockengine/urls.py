from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.test, name='test'),
    url(r'^home/', views.portfolio, name='portfolio'),
    url(r'^refresh$', views.refresh, name='refreshdb'),
]