from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'stocksite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^stock/', include('stockengine.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
