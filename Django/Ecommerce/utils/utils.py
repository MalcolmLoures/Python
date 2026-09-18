def formata_preco (valor):
    print ('valor: ', valor)
    if not valor:
        return f'R$--'.replace('.', ',') 
        
    return f'R$ {valor:.2f}'.replace('.', ',')

def cart_total_qtd (carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_total_valor (carrinho):
    return sum( [   
                    item['preco_quantitativo_promocional'] if item['preco_quantitativo_promocional'] 
                    else item['preco_quantitativo']  
                    for item in carrinho.values() 
                ] )