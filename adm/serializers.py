from .choices import FINALIZADO
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


class ItemVendaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemVenda
        fields = ('id', 'produto_servico', 'venda',
                  'quantidade', 'total', 'total_comissao')
        depth = 1


class ItemVendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemVenda
        fields = ('id', 'produto_servico', 'venda',
                  'quantidade', 'total', 'total_comissao')


class VendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venda
        fields = ['id', 'data_criacao', 'vendedor', 'cliente', 'situacao',
                  'valor_total', 'valor_comissao_total']

    def calcula_comissao_da_venda(self, venda):
        """
            Calcula comissão dos itens da venda, de acordo com o horário atual.

        """

        id_venda = venda.id
        # pega hora atual:
        hora_atual = datetime.today().time().replace(second=0, microsecond=0)
        # intervalo um
        inicio_intervalo_1 = datetime.strptime('00:00', '%H:%M').time()
        fim_intervalo_1 = datetime.strptime('12:00', '%H:%M').time()
        # intervalo dois
        inicio_intervalo_2 = datetime.strptime('12:01', '%H:%M').time()
        fim_intervalo_2 = datetime.strptime('23:59', '%H:%M').time()

        # intervalo 1: 00:00 as 12:00
        intervalo_1_ativo = False
        # intervalo 2: 12:01 as 23:59
        intervalo_2_ativo = False

        # Se vender entre 00:00 e 12:00 a comissão máxima é de 5% por item venda.
        if hora_atual >= inicio_intervalo_1 and hora_atual <= fim_intervalo_1:
            intervalo_1_ativo = True

        # Venda entre 12:01 e 23:59 a comissão é no mínimo 4%.
        elif hora_atual >= inicio_intervalo_2 and hora_atual <= fim_intervalo_2:
            intervalo_2_ativo = True

        # captura itens da venda atual
        lista_item_venda = ItemVenda.objects.filter(venda_id=id_venda)

        # itera sobre os itens venda, verificando a restrição de comissao e recalcula.
        for item_venda in lista_item_venda:

            if intervalo_1_ativo:
                # entre 00:00 e 12:00 a comissão máxima é de 5% por item venda.
                # se passar do maximo, aplicar o maximo e recalcular comissao do item
                if item_venda.produto_servico.comissao > Decimal(5.0):
                    item_venda.calcula_total_comissao_item(
                        comissao_reaplicada=Decimal(5.0))
                else:
                    item_venda.calcula_total_comissao_item()

            elif intervalo_2_ativo:
                # entre 12:01 e 23:59 a comissão é no mínimo 4%.
                # se menor que 4%, aplicar o minimo e recalcular comissao do item
                if item_venda.produto_servico.comissao < Decimal(4.0):
                    item_venda.calcula_total_comissao_item(
                        comissao_reaplicada=Decimal(4.0))
                else:
                    item_venda.calcula_total_comissao_item()

            item_venda.save()

    def create(self, validated_data):
        """
            Metodo que modifica o create method do serializer para calcular 
            a comissão dos itens relacionados.
        """
        venda_obj = Venda.objects.create(**validated_data)
        situacao_atualizada = venda_obj.situacao

        # ao finalizar venda, verificar restriçoes de horario para dar comissão no item da venda:
        if venda_obj.situacao == FINALIZADO:
            self.calcula_comissao_da_venda(venda_obj)

        return venda_obj

    def update(self, instance, validated_data):
        """
            Modifica o update method do serializer para calcular comissao dos itens da venda.
        """
        # ao finalizar venda (status FINALIZADO), verificar itens se realmente estao seguindo a restrição de horario:
        id_venda = instance.id
        situacao_atualizada = validated_data['situacao']

        venda_atual = Venda.objects.filter(id=id_venda).first()

        # ao finalizar venda, verificar restriçoes de horario para dar comissão no item da venda:
        if situacao_atualizada == FINALIZADO:
            self.calcula_comissao_da_venda(venda_atual)

        instance = super().update(instance, validated_data)
        return instance


class VendaListSerializer(serializers.ModelSerializer):
    list_itens = ItemVendaListSerializer(source='itemvenda_set', many=True)

    class Meta:
        model = Venda
        fields = ['id', 'data_criacao', 'vendedor', 'cliente', 'situacao',
                  'valor_total', 'valor_comissao_total', 'list_itens']
        depth = 1
