from .serializers import ClienteSerializer, ItemVendaSerializer, ProdutoServicoSerializer, VendaSerializer, VendedorSerializer
from .models import Cliente, ItemVenda, ProdutoServico, Venda, Vendedor
from django.shortcuts import render
from rest_framework import viewsets


# Create your views here.
class ProdutoServicoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProdutoServico.objects.all().order_by('-id')
    serializer_class = ProdutoServicoSerializer
    # permission_classes = [permissions.IsAuthenticated]


class VendedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Vendedor.objects.all().order_by('-id')
    serializer_class = VendedorSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Cliente.objects.all().order_by('-id')
    serializer_class = ClienteSerializer
    # permission_classes = [permissions.IsAuthenticated]


class VendaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Venda.objects.all().order_by('-id')
    serializer_class = VendaSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ItemVendaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemVenda.objects.all().order_by('-id')
    serializer_class = ItemVendaSerializer
    # permission_classes = [permissions.IsAuthenticated]