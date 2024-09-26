from django.urls import path
from . import views
from .views import device_status_view, edit_frequency_view, edit_frequency_step_view, edit_gain_view, edit_mute_view, logs_view, get_device_alerts, edit_device_view

urlpatterns = [
    path('status/', device_status_view, name='device_status'),
    path('edit/', edit_device_view, name='edit_device'),
    path('edit/frequency/', edit_frequency_view, name='edit_frequency'),
    path('edit/frequency_step/', edit_frequency_step_view, name='edit_frequency_step'),
    path('edit/gain/', edit_gain_view, name='edit_gain'),
    path('edit/mute/', edit_mute_view, name='edit_mute'),
    path('logs/', logs_view, name='logs'),
    path('alerts/', get_device_alerts, name='get_device_alerts'),
]
