from .choices import SITUACAO_VENDA_CHOICES
from django.db import models


class ProdutoServico(models.Model):
    descricao = models.CharField(max_length=150, verbose_name='Descrição')
    codigo_barras = models.IntegerField(verbose_name='Código de Barras')
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Preço Unitário')
    comissao = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='% Comissão')

    def __str__(self):
        return self.descricao
    

class Vendedor(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome')
    telefone = models.CharField(max_length=11, verbose_name='Telefone')

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Nome')
    telefone = models.CharField(max_length=11, verbose_name='Telefone')

    def __str__(self):
        return self.nome

# todo: O total de comissão da venda é o total das somas das comissões dos itens da venda
class Venda(models.Model):
    data_criacao = models.DateTimeField(auto_now=True, verbose_name='Data criação')
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True, verbose_name='Vendedor', on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, verbose_name='Cliente', on_delete=models.PROTECT)
    situacao = models.IntegerField(choices=SITUACAO_VENDA_CHOICES, verbose_name='Situação', default=1)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Total Venda')
    valor_comissao_total = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Valor Total de Comissão')

    def calcula_valor_total(self):
        list_total = self.itemvenda_set.filter(venda=self).values_list('total', flat=True)
        total = sum(list_total)
        self.valor_total = total

    def calcula_valor_comissao_total(self):
        list_comissao_total = self.itemvenda_set.filter(venda=self).values_list('total_comissao', flat=True)
        total_comissao = sum(list_comissao_total)
        self.valor_comissao_total = total_comissao

    def save(self, *args, **kwargs):
        # super(Venda, self).save(*args, **kwargs)
        self.calcula_valor_total()
        self.calcula_valor_comissao_total()
        super(Venda, self).save(*args, **kwargs)


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, verbose_name='Venda', on_delete=models.PROTECT)
    produto_servico = models.ForeignKey(ProdutoServico, verbose_name='Produto/Serviço', on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1, verbose_name='Quantidade')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Total')
    total_comissao = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Total de Comissão')

    def calcula_total_item(self):
        self.total = (self.produto_servico.preco_unitario * self.quantidade)
    
    def calcula_total_comissao_item(self):
        percentual = self.produto_servico.comissao
        calculo_comissao = self.total * (percentual/100)
        self.total_comissao = calculo_comissao

    def save(self, *args, **kwargs):
        self.calcula_total_item()
        self.calcula_total_comissao_item()
        super(ItemVenda, self).save(*args, **kwargs)
