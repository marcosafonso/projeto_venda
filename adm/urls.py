from django.conf.urls import include
from django.urls import path
from .import views
from rest_framework import routers
from .views import ProdutoServicoViewSet, VendedorViewSet, ClienteViewSet, VendaViewSet, \
    ItemVendaViewSet

router = routers.DefaultRouter()
router.register(r'produto_servicos', ProdutoServicoViewSet)
router.register(r'vendedor', VendedorViewSet)
router.register(r'cliente', ClienteViewSet)
router.register(r'venda', VendaViewSet)
router.register(r'item_venda', ItemVendaViewSet)

urlpatterns=[
    #your paths go here
    path('', include(router.urls)),
]