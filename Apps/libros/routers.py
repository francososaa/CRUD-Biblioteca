
from rest_framework import routers

from .views import AutorAPIView, LibroAPIView

router = routers.DefaultRouter()
router.register(r'autor', AutorAPIView, basename='autor')
router.register(r'libro', LibroAPIView, basename='libro')


urlpatterns = router.urls