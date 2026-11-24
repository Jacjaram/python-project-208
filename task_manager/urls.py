from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse
import sentry_sdk


def trigger_error(request):
    try:
        1 / 0
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
    return HttpResponse("Error enviado a Sentry", status=500)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', include('users.urls')),
    path('', include('tasks.urls')),
    path('sentry-debug/', trigger_error),
]