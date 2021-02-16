from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Venda, ItemVenda, Vendedor, Cliente, ProdutoServico
from decimal import Decimal

class RealizarVendaTestCase(TestCase):
    """
        Testa a realização de uma venda.
    """
    def setUp(self):
        vendedor = Vendedor.objects.create(nome="Mario Bras", telefone="27998643670")
        cliente = Cliente.objects.create(nome="Alan Silva", telefone="11998642540")

        produto = ProdutoServico.objects.create(descricao="Lápis", codigo_barras=123,
                                      preco_unitario=2.00, comissao=4.00)
                                      
        venda = Venda.objects.create(vendedor=vendedor, cliente=cliente, situacao=1)
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

