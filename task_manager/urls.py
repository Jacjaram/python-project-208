from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse
import sentry_sdk


def trigger_error(request):
    sentry_sdk.capture_message("Prueba de Bugsink desde Render", level="error")
    return HttpResponse("Mensaje enviado a Sentry", status=200)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', include('users.urls')),
    path('', include('tasks.urls')),
    path('sentry-debug/', trigger_error),
]
