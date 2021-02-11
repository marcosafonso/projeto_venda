from rest_framework import serializers
from .models import ProdutoServico, Vendedor, Cliente, Venda, ItemVenda


class ProdutoServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProdutoServico
        fields = ['id', 'descricao', 'codigo_barras', 'preco_unitario', 'comissao']


class VendedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendedor
        fields = ['id', 'nome', 'telefone']


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'telefone']


class VendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venda
        fields = ['id', 'data_criacao', 'vendedor', 'cliente', 'situacao', 'valor_total', 'valor_comissao_total']


class ItemVendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemVenda
        fields = ['id', 'venda', 'produto_servico', 'quantidade', 'total', 'total_comissao']



