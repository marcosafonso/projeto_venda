from django.core.checks import messages
from .choices import FINALIZADO
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ClienteSerializer, ItemVendaListSerializer, ItemVendaSerializer, ProdutoServicoSerializer, VendaListSerializer, VendaSerializer, VendedorSerializer
from .models import Cliente, ItemVenda, ProdutoServico, Venda, Vendedor
from django.shortcuts import render
from rest_framework import response, viewsets
from rest_framework.utils import json
from datetime import datetime
import operator


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


class VendaListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Venda.objects.all().order_by('-id')
    serializer_class = VendaListSerializer
    http_method_names = ['get']
    # permission_classes = [permissions.IsAuthenticated]


class VendaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Venda.objects.all().order_by('-id')
    serializer_class = VendaSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ItemVendaListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemVenda.objects.all().order_by('-id')
    serializer_class = ItemVendaListSerializer
    http_method_names = ['get']

    # def get_queryset(self):
    #     """
    #         override get queryset
    #     """
    #     queryset = ItemVenda.objects.all().order_by('-id')
    #     venda_pk = self.request.query_params.get('venda_pk', None)
    #     if venda_pk is not None:
    #         queryset = queryset.filter(venda_id=venda_pk)
    #     return queryset


class ItemVendaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ItemVenda.objects.all().order_by('-id')
    serializer_class = ItemVendaSerializer
    # permission_classes = [permissions.IsAuthenticated]


# 1. Dado um intervalo de tempo, quanto de comissão um vendedor tem direito?
@api_view(('GET',))
def pesquisa_comissao_vendedor(request, pk=None):
    """
        Pesquisa em um intervalo de datas, o valor de comissao pago ao vendedor.
        Url: 127.0.0.1:8000/adm/pesquisa_comissao_vendedor
        Exemplo de json de requisicao:
        {
            "data_inicio": "10/02/2021",
            "data_fim": "14/02/2021",
            "vendedor": "2798635640" # pesquisado pelo telefone vendedor.
        }
    """
    try:
        # formato nosso utf-8
        body_decode = request.body.decode('utf-8')
        json_objeto = json.loads(body_decode)

        data_inicio_str = json_objeto['data_inicio']
        data_fim_str = json_objeto['data_fim']
        vendedor_str = json_objeto['vendedor']

        data_inicio = datetime.strptime(data_inicio_str,  '%d/%m/%Y')
        data_fim = datetime.strptime(data_fim_str,  '%d/%m/%Y')

        vendedor_obj = Vendedor.objects.filter(telefone=vendedor_str).first()

        total_comissao = Venda.objects.filter(
            data_criacao__date__lte=data_fim, data_criacao__date__gte=data_inicio, situacao=FINALIZADO,
            vendedor=vendedor_obj).values_list('valor_comissao_total', flat=True)
        total_comissao = sum(total_comissao)

        mensagem = {'total_comisao': total_comissao}
        return Response(mensagem, status=200, content_type='application/json')

    except Exception as e:
        # Retorna um erro
        erro = {"erro": "A requisição tem corpo inválido!"}
        return Response(erro,
                        content_type='application/json', status=400)


# 2. Quais produtos e serviços um determinado cliente comprou num intervalo de tempo?
@api_view(('GET',))
def pesquisa_compras_cliente(request, pk=None):
    """
        Mostra produtos serviços que um cliente comprou num intervalo de tempo.
        Url: 127.0.0.1:8000/adm/pesquisa_compras_cliente
        {
            "data_inicio": "10/02/2021",
            "data_fim": "14/02/2021",
            "cliente": "33280968" # usado telefone para pesquisar cliente.
        }
    """
    try:
        # formato nosso utf-8
        body_decode = request.body.decode('utf-8')
        json_objeto = json.loads(body_decode)

        data_inicio_str = json_objeto['data_inicio']
        data_fim_str = json_objeto['data_fim']
        cliente_str = json_objeto['cliente']

        data_inicio = datetime.strptime(data_inicio_str,  '%d/%m/%Y')
        data_fim = datetime.strptime(data_fim_str,  '%d/%m/%Y')

        cliente_obj = Cliente.objects.filter(telefone=cliente_str).first()

        lista_itens_vendas = ItemVenda.objects.filter(
            venda__data_criacao__date__lte=data_fim, venda__data_criacao__date__gte=data_inicio, venda__situacao=FINALIZADO,
            venda__cliente=cliente_obj).values_list('produto_servico__descricao', flat=True).distinct()

        print(lista_itens_vendas)
        mensagem = {'Produtos e serviços adquiridos': lista_itens_vendas}
        return Response(mensagem, status=200, content_type='application/json')

    except Exception as e:
        # Retorna um erro
        erro = {"erro": "A requisição tem corpo inválido!"}
        return Response(erro,
                        content_type='application/json', status=400)


# 3. Quais os produtos e serviços mais vendidos num dado intervalo de datas? Listar em ordem decrescente
@api_view(('GET',))
def pesquisa_mais_vendidos(request, pk=None):
    """
        Pesquisa os produtos e serviços mais vendidos num intervalo de data informado no json de requisição.
        Url: 127.0.0.1:8000/adm/pesquisa_mais_vendidos
        Exemplo do json de requisição dos produtos mais vendidos: 
        {
           "data_inicio": "10/02/2021",
           "data_fim": "14/02/2021"
        }
    """
    try:
        # formato nosso utf-8
        body_decode = request.body.decode('utf-8')
        json_objeto = json.loads(body_decode)

        data_inicio_str = json_objeto['data_inicio']
        data_fim_str = json_objeto['data_fim']

        data_inicio = datetime.strptime(data_inicio_str,  '%d/%m/%Y')
        data_fim = datetime.strptime(data_fim_str,  '%d/%m/%Y')


        lista_itens_vendas = ItemVenda.objects.filter(
            venda__data_criacao__date__lte=data_fim, venda__data_criacao__date__gte=data_inicio, venda__situacao=FINALIZADO)
            # .values_list('produto_servico_id', flat=True).distinct()

        ids_itens_vendidos = lista_itens_vendas.values_list('produto_servico_id', flat=True).distinct()

        relatorio_dic = {}
        for item_vendido in ids_itens_vendidos:
            produto_obj = ProdutoServico.objects.filter(id=item_vendido).first()
            qtd = lista_itens_vendas.filter(produto_servico_id=item_vendido).count()
            
            relatorio_dic['id: '+ str(produto_obj.id) + ' - ' + produto_obj.descricao] = qtd

        relatorio_ordenado_d = dict( sorted(relatorio_dic.items(), key=operator.itemgetter(1), reverse=True))

        mensagem = {'Produtos e serviços adquiridos': relatorio_ordenado_d }
        return Response(mensagem, status=200, content_type='application/json')

    except Exception as e:
        # Retorna um erro
        erro = {"erro": "A requisição tem corpo inválido!"}
        print(e)
        return Response(erro,
                        content_type='application/json', status=400)
