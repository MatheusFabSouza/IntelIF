from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),
    path("logout/", views.logout, name="logout"),

    path("google/login/", views.google_login, name="google_login"),
    path("google/callback/", views.google_callback, name="google_callback"),

    path("perfil/integracoes/classroom/sincronizar/", views.sincronizar_classroom, name="sincronizar_classroom"),
    path("perfil/", views.perfil, name="perfil"),
]