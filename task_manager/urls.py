from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse


def trigger_error(request):
    division_by_zero = 1 / 0
    return HttpResponse("No deberías ver esto")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', include('users.urls')),
    path('', include('tasks.urls')),
    path('sentry-debug/', trigger_error),
]