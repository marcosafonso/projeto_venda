from django.urls import reverse
from rest_framework import status
from .serializers import ClienteSerializer
from rest_framework.test import APIClient
from django.test import TestCase

from django.test import TestCase
from .models import Venda, ItemVenda, Vendedor, Cliente, ProdutoServico
from decimal import Decimal


class RealizarVendaTestCase(TestCase):
    """
        Testa a realização de uma venda, com calculo de comissão e valor total da venda.
    """

    def setUp(self):
        vendedor = Vendedor.objects.create(
            nome="Mario Bras", telefone="27998643670")
        cliente = Cliente.objects.create(
            nome="Alan Silva", telefone="11998642540")

        produto = ProdutoServico.objects.create(descricao="Lápis", codigo_barras=123,
                                                preco_unitario=2.00, comissao=4.00)

        venda = Venda.objects.create(
            vendedor=vendedor, cliente=cliente, situacao=1)
        item = ItemVenda.objects.create(venda=venda, produto_servico=produto,
                                        quantidade=2)
        item.calcula_total_comissao_item()
        item.save()
        venda.save()

    def test_realiza_venda(self):
        """Checa se valor da venda será correspondente ao item vendido"""
        venda = Venda.objects.get(id=1)

        # cat = Animal.objects.get(name="cat")
        self.assertEqual(venda.valor_total, round(Decimal(4.00), 2))
        self.assertEqual(venda.valor_comissao_total, round(Decimal(0.16), 2))


class ClientesApiTest(TestCase):

    # pega APiClient para testar chamada de urls
    def setUp(self):
        self.client = APIClient()

    # cria clientes e testa requisição na url de get clientes
    def test_cliente_list(self):
        Cliente.objects.create(nome='Fulano Oliveira', telefone='27998645678')
        Cliente.objects.create(nome='Cicrano Oliveira', telefone='11995645677')

        res = self.client.get("http://localhost:8000/adm/cliente/")

        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # testa criar novo cliente pela api e se ele existe no banco
    def test_create_cliente_sucessfull(self): 
        payload = {'nome': 'Johnson', 'telefone': '4130665890'}
        self.client.post("http://localhost:8000/adm/cliente/", payload)
        exists = Cliente.objects.filter(
            nome=payload['nome'],
        ).exists()
        self.assertTrue(exists)
