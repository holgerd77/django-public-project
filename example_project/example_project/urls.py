from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
import django.views

from public_project.urls import urlpatterns

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]