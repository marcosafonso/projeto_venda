from .models import ProdutoServico, Vendedor, Cliente, Venda, ItemVenda
from django.contrib import admin

# Register your models here.
admin.site.register(ProdutoServico)
admin.site.register(Vendedor)
admin.site.register(Cliente)


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda

class VendaAdmin(admin.ModelAdmin):
    inlines = [
        ItemVendaInline,
    ]
admin.site.register(Venda, VendaAdmin)

#admin.site.register(ItemVenda)
