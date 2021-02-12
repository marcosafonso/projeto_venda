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


class ItemVendaSerializer(serializers.ModelSerializer):
    """ Fundamental ter o id aqui para fazer update ao usar como nested objects (entenda formset) em
    um cadastro Pai (nesse caso, cadastro de Produto)."""
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ItemVenda
        fields = ('id', 'produto_servico', 'quantidade', 'total', 'total_comissao')


class VendaSerializer(serializers.ModelSerializer):
    list_item_venda = ItemVendaSerializer(source='itemvenda_set',
        many=True, read_only=False)
    class Meta:
        model = Venda
        fields = ['id', 'data_criacao', 'vendedor', 'cliente', 'situacao',
                  'valor_total', 'valor_comissao_total', 'list_item_venda']
        depth = 1
    
    """Funcao feita para criar os itens venda"""
    def cria_itens_venda(self, itens_venda, venda):
        for item in itens_venda:
            fornec = ItemVenda.objects.create(**item, venda=venda)
            
    """ Criar metodo que simular formset com o cadastro de itens da venda """
    def create(self, validated_data):
        print(validated_data)
        itens_venda = validated_data['itemvenda_set']
        del validated_data['itemvenda_set']

        venda = Venda.objects.create(**validated_data)

        self.cria_itens_venda(itens_venda, venda)

    """ Método que atualiza venda, e seus respectivos itens.
        Atualiza, quando tem o id, quando não, cria um novo item para aquela venda.
    """
    def update(self, instance, validated_data):
        itens_venda = validated_data['itemvenda_set']
        del validated_data['itemvenda_set']

        instance = super().update(instance, validated_data)

        for item in itens_venda:
            item_id = item.get('id', None)

            if item_id:
                item_obj = ItemVenda.objects.get(id=item_id, venda=instance)
                item_obj.venda = item.get('venda', item_obj.venda)
                item_obj.save()
            else:
                ItemVenda.objects.create(venda=instance, **item)

        return instance



