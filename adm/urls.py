from django.conf.urls import include
from django.urls import path
from .import views
from rest_framework import routers
from .views import ProdutoServicoViewSet, VendedorViewSet, ClienteViewSet, VendaViewSet,\
    ItemVendaViewSet, pesquisa_comissao_vendedor, pesquisa_compras_cliente, pesquisa_mais_vendidos

router = routers.DefaultRouter()
router.register(r'produto_servico', ProdutoServicoViewSet)
router.register(r'vendedor', VendedorViewSet)
router.register(r'cliente', ClienteViewSet)
router.register(r'venda', VendaViewSet)
router.register(r'item_venda', ItemVendaViewSet)

urlpatterns=[
    #your paths go here
    path('', include(router.urls)),
    path('pesquisa_comissao_vendedor', pesquisa_comissao_vendedor, name='pesquisa_comissao_vendedor'),
    path('pesquisa_compras_cliente', pesquisa_compras_cliente, name='pesquisa_compras_cliente'),
    path('pesquisa_mais_vendidos', pesquisa_mais_vendidos, name='pesquisa_mais_vendidos')
]