from django.contrib import admin
from django.urls import path
from myapp.views import dashboard, poll_view, access_denied_view, thank_you_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
    path('poll/<uuid:poll_id>/', poll_view, name='poll_url'),
    path('access-denied/', access_denied_view, name='access_denied'),
    path('thank-you/', thank_you_view, name='thank_you'),
]
