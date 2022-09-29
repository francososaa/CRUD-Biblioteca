from rest_framework import routers

from .views import UsuarioApiView

router = routers.DefaultRouter()
router.register(r'users',UsuarioApiView, basename='usuario')

urlpatterns = router.urls

