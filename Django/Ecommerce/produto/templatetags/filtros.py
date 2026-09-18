from django import template 
from utils import utils 

register = template.Library()

@register.filter
def formata_preco (valor):
    return utils.formata_preco(valor)
   # return f'R$ {valor:.2f}'.replace('.', ',')

@register.filter
def cart_total_qtd (session):
    return utils.cart_total_qtd(session)

@register.filter
def cart_total_valor(session):
    return utils.cart_total_valor(session)