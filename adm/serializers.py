from rest_framework import serializers
from .models import ProdutoServico, Vendedor, Cliente, Venda, ItemVenda
from decimal import Decimal
from datetime import datetime


class ProdutoServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProdutoServico
        fields = ['id', 'descricao', 'codigo_barras',
                  'preco_unitario', 'comissao']


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
        fields = ('id', 'produto_servico', 'venda',
                  'quantidade', 'total', 'total_comissao')
    
    # def create(self, validated_data):
    #     """ Modificar a comissão de acordo com horário de realização. Baseado na Data criação."""
    #     produto_servico = validated_data['produto_servico']
    #     venda = validated_data['venda']

    #     #pega hora atual:
    #     hora_atual = datetime.today().time().replace(second=0, microsecond=0)
    #     # intervalo um
    #     meia_noite =  datetime.strptime('00:00', '%H:%M').time()
    #     meio_dia =  datetime.strptime('12:00', '%H:%M').time()
    #     # intervalo dois
    #     meio_dia_um =  datetime.strptime('12:01', '%H:%M').time()
    #     onze_cinquenta_nove =  datetime.strptime('23:59', '%H:%M').time()

    #     # Se vender entre 00:00 e 12:00 a comissão máxima é de 5% por item venda.
    #     if hora_atual >= meia_noite and hora_atual <= meio_dia:
    #         print("antes do meio-dia")
        
    #     # Venda entre 12:01 e 23:59 a comissão é no mínimo 4%.
    #     elif hora_atual >= meio_dia_um and hora_atual <= onze_cinquenta_nove:
    #         print("depois do meio-dia HAHA")
    #     # if produto_servico.comissao > round(Decimal(5.00), 2):
            
    #     return ItemVenda.objects.create(**validated_data)

    # def validate(self, data):
    #     """
    #     Chek that the start is before the stop.
    #     """

    #     if data['start_date'] > data['end_date']:
    #         raise serializers.ValidationError("finish must occur after start")
    #     return data


class VendaSerializer(serializers.ModelSerializer):
    # list_item_venda = ItemVendaSerializer(source='itemvenda_set',
    #     many=True, read_only=True)

    class Meta:
        model = Venda
        fields = ['id', 'data_criacao', 'vendedor', 'cliente', 'situacao',
                  'valor_total', 'valor_comissao_total']
        # depth = 1

    # """Funcao feita para criar os itens venda"""
    # def cria_itens_venda(self, itens_venda, venda):
    #     for item in itens_venda:
    #         fornec = ItemVenda.objects.create(**item, venda=venda)

    # # """ Criar metodo que simular formset com o cadastro de itens da venda """
    # def create(self, validated_data):
    #     print(validated_data)
    #     itens_venda = validated_data['itemvenda_set']
    #     del validated_data['itemvenda_set']

    #     venda = Venda.objects.create(**validated_data)

    #     self.cria_itens_venda(itens_venda, venda)

    #     venda.save()

    # # """ Método que atualiza venda, e seus respectivos itens.
    # #     Atualiza, quando tem o id, quando não, cria um novo item para aquela venda.
    # # """
    # def update(self, instance, validated_data):
    #     itens_venda = validated_data['itemvenda_set']
    #     del validated_data['itemvenda_set']

    #     instance = super().update(instance, validated_data)

    #     for item in itens_venda:
    #         item_id = item.get('id', None)

    #         if item_id:
    #             item_obj = ItemVenda.objects.get(id=item_id, venda=instance)
    #             item_obj.venda = item.get('venda', item_obj.venda)
    #             item_obj.save()
    #         else:
    #             ItemVenda.objects.create(venda=instance, **item)

    #     return instance
