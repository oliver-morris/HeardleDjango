from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "heardle"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("heardle/", views.heardle, name="heardle"),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
