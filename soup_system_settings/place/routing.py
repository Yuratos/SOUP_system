from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/place/(?P<place_name>[^/]+)/$', consumers.PlaceConsumer.as_asgi()),
]