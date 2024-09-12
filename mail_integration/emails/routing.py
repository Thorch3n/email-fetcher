from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/email-progress/(?P<email_id>\d+)/$', consumers.EmailProgressConsumer.as_asgi()),
]