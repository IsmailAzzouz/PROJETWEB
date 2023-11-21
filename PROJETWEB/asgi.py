"""
ASGI config for PROJETWEB project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Game.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJETWEB.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})# Ajoutez ceci pour la gestion des fichiers statiques
from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import re_path, path

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter([])
        ),
    }
)

if settings.DEBUG:
    application = ProtocolTypeRouter(
        {
            "http": get_asgi_application(),
            "websocket": AuthMiddlewareStack(
                URLRouter([])
            ),
            # Ajoutez ceci pour la gestion des fichiers statiques
            "static": views.serve,
        }
    )