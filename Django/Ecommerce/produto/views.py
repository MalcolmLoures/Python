from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from perfil.models import Perfil
from django.db.models import Q

from pprint import pprint

# Create your views here.
class ListaProdutos(ListView): #ListView
    model = models.Produto
    template_name = 'produto\lista.html'
    context_object_name = 'produtos'
    paginate_by = 10
    
class Busca (ListaProdutos):
    
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo')
        qs = super().get_queryset(*args, **kwargs)
        if not termo:
            return super().get_queryset()
        
        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )
        
        return qs
        
    
class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto\detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
    
class AdicionarAoCarrinho(View):
    def get(self, request, *args, **kwargs):
        
        # messages.error(
        #     self.request,
        #     'Erro de teste'
        # )
        # return redirect(self.request.META['HTTP_REFERER'])
    
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')
        
        if not variacao_id:
            messages.error(self.request, 'Variação nao foi selecionada')
            return redirect(http_referer)
        
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        
        if variacao.estoque < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(http_referer)
        
        produto = variacao.produto
        
        produto_id = produto.id 
        produto_nome = produto.nome
        variacao_nome = variacao.name or ''
        preco_unitario = variacao.preco
        preco_quantitativo = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        preco_quantitativo_promocional = variacao.preco_promocional 
        quantidade = 1
        slug = produto.slug 
        imagem = produto.imagem
        
        if imagem:
            imagem = imagem.url
        else:
            imagem = ''
        
        #criação do carrinho na sessão do usuario
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        
        carrinho = self.request.session['carrinho']
        
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1
            
            if variacao.estoque < quantidade_carrinho :
                messages.warning(self.request, f'Estoque insuficiente para {quantidade_carrinho} no produto {produto_nome}. Adicionamos {variacao.estoque} no seu carrinho.')
                quantidade_carrinho = variacao.estoque
                
            carrinho[variacao_id]['imagem'] = imagem
                
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                'produto_id' : produto_id
                ,'produto_nome' : produto_nome	
                ,'variacao_nome' : variacao_nome
                ,'variacao_id' : variacao_id
                ,'preco_unitario' : preco_unitario
                ,'preco_quantitativo': preco_quantitativo
                ,'preco_unitario_promocional' : preco_unitario_promocional
                ,'preco_quantitativo_promocional' : preco_quantitativo_promocional
                ,'quantidade' : quantidade
                ,'slug' : slug
                ,'imagem' : imagem
            }
        
        self.request.session.save()
        messages.success(self.request, f'Produto {produto_nome} adicionado ao seu carrinho.')
        print("Carrinho atualizado:")   
        pprint(carrinho) 
        return redirect(http_referer)    
 

class RemoverDoCarrinho(View):
    def get(self, request, *args, **kwargs):
        
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variacao_id = self.request.GET.get('vid')
        
        if not variacao_id:
              return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)
        
        if variacao_id not in self.request.session.get('carrinho'):
            return redirect(http_referer)
    
        carrinho = self.request.session['carrinho']
        messages.success(
            self.request,
            f'Produto {carrinho[variacao_id]["produto_nome"]} {carrinho[variacao_id]["variacao_nome"]} removido do seu carrinho.'
        )
        
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        
        return redirect(http_referer) # retorna para a pagina que estava anteriormente


class Carrinho(View):
    def get(self, request, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho')
        }
        return render(self.request, 'produto/carrinho.html', contexto)


class Finalizar(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Finalizar')

class ResumoCompra(View):
    def get(self, request, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        
        perfil = Perfil.objects.filter(usuario= self.request.user).exists()
        
        if not perfil:
            messages.error (
                self.request,
                'Usuário sem perfil'
            )
            return redirect("perfil:criar")
            
        carrinho = self.request.session.get('carrinho')
        
        if not carrinho:
            messages.error (
                self.request,
                'Carrinho vazio'
            )
            return redirect("produto:lista")
        
        contexto = {
            'usuario': self.request.user,
            'carrinho': carrinho
        }
        return render(self.request, 'produto/resumo.html', contexto)

