import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import medical.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        medical.routing.websocket_urlpatterns
    ),
})
