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
    # """ Fundamental ter o id aqui para fazer update ao usar como nested objects (entenda formset) em
    # um cadastro Pai (nesse caso, cadastro de Produto)."""
    # id = serializers.IntegerField(required=False)
    
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
    def calcula_comissao_da_venda(self, venda):
        id_venda = venda.id
        #pega hora atual:
        hora_atual = datetime.today().time().replace(second=0, microsecond=0)
        # intervalo um
        inicio_intervalo_1 =  datetime.strptime('00:00', '%H:%M').time()
        fim_intervalo_1 =  datetime.strptime('12:00', '%H:%M').time()
        # intervalo dois
        inicio_intervalo_2=  datetime.strptime('12:01', '%H:%M').time()
        fim_intervalo_2 =  datetime.strptime('23:59', '%H:%M').time()

        intervalo_1_ativo = False
        intervalo_2_ativo = False

        # Se vender entre 00:00 e 12:00 a comissão máxima é de 5% por item venda.
        if hora_atual >= inicio_intervalo_1 and hora_atual <= fim_intervalo_1:
            print("antes do meio-dia")
            intervalo_1_ativo = True
        
        # Venda entre 12:01 e 23:59 a comissão é no mínimo 4%.
        elif hora_atual >= inicio_intervalo_2 and hora_atual <= fim_intervalo_2:
            print("depois do meio-dia HAHA")
            intervalo_2_ativo = True

        lista_item_venda = ItemVenda.objects.filter(venda_id=id_venda)

        # itera sobre os itens venda, verificando a restrição de comissao e recalcula.
        for item_venda in lista_item_venda:

            if intervalo_1_ativo:
                # entre 00:00 e 12:00 a comissão máxima é de 5% por item venda.
                # se passar do maximo, aplicar o maximo e recalcular comissao do item
                if item_venda.produto_servico.comissao > Decimal(5.0):
                    item_venda.calcula_total_comissao_item(comissao_reaplicada=Decimal(5.0))
                else:
                    item_venda.calcula_total_comissao_item()
            
            elif intervalo_2_ativo:
                # entre 12:01 e 23:59 a comissão é no mínimo 4%.
                # se menor que 4%, aplicar o minimo e recalcular comissao do item
                if item_venda.produto_servico.comissao < Decimal(4.0):
                    print("Produto nao atinge comissao minima")
                    item_venda.calcula_total_comissao_item(comissao_reaplicada=Decimal(4.0))
                else:
                    print("mais do que o minimo!!")
                    item_venda.calcula_total_comissao_item()

            item_venda.save()

    def create(self, validated_data):

        venda_obj = Venda.objects.create(**validated_data)
        situacao_atualizada = venda_obj.situacao

        # ao finalizar venda, verificar restriçoes de horario para dar comissão no item da venda:
        # TODO: pode nao ser necessaria essa execucao de calculo_comissao:
        if venda_obj.situacao == FINALIZADO:
            print("pronto para calcular comissao no create")
            self.calcula_comissao_da_venda(venda_obj)
            print("calculou!!!!")

        return venda_obj
        
    # # """ Método que atualiza venda, e seus respectivos itens.
    # #     Atualiza, quando tem o id, quando não, cria um novo item para aquela venda.
    # # """
    def update(self, instance, validated_data):
        # ao finalizar venda (status FINALIZADO), verificar itens se realmente estao seguindo a restrição de horario:
        id_venda = instance.id
        situacao_atualizada = validated_data['situacao']

        intervalo_1_ativo = False
        intervalo_2_ativo = False

        venda_atual = Venda.objects.filter(id=id_venda).first()

        # ao finalizar venda, verificar restriçoes de horario para dar comissão no item da venda:
        if situacao_atualizada == FINALIZADO :
            self.calcula_comissao_da_venda(venda_atual)
        else:
            print("situacao finalizada repetiu")

        instance = super().update(instance, validated_data)
        return instance


class VendaListSerializer(serializers.ModelSerializer):
    list_itens = ItemVendaListSerializer(source='itemvenda_set', many=True)
    
    class Meta:
        model = Venda
        fields = ['id', 'data_criacao', 'vendedor', 'cliente', 'situacao',
                  'valor_total', 'valor_comissao_total', 'list_itens']
        depth = 1