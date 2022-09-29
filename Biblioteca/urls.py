from django.contrib import admin
from django.urls import path, include

from Apps.usuarios.views import Login, Logout, CreateUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Apps.usuarios.routers')),
    path('api/', include('Apps.libros.routers')),
    path('api/register/', CreateUser.as_view(), name='create_user'),
    path('auth/login/',Login.as_view(), name='login'),
    path('auth/logout/', Logout.as_view(), name='logout'),
    path('api_authorization/',include('rest_framework.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
