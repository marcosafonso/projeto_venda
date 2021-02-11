from .serializers import ProdutoServicoSerializer
from .models import ProdutoServico
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