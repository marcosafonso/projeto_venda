from django.conf.urls import include
from django.urls import path
from .import views
from rest_framework import routers
from .views import ProdutoServicoViewSet

router = routers.DefaultRouter()
router.register(r'produto_servicos', ProdutoServicoViewSet)


urlpatterns=[
    #your paths go here
    path('', include(router.urls)),
]