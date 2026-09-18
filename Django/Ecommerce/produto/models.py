from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from utils import utils

# Create your models here.
    
class Produto (models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField(default='')
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(default=0)
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples')
        )
    )
    
    def __str__(self):
        return self.nome
    
    @staticmethod
    def resize_image(img, new_with=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_w, original_h = img_pil.size
        
        if original_w <= new_with:
            img_pil.close()
            print ('retornando...')
            return
        
        new_h = round( new_with * original_h / original_w )
        new_img = img_pil.resize((new_with, new_h), resample=Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
        print( 'imagem redimensionada')
        
        
    def save (self, *args, **kwargs):
        
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug
            
        super().save(*args, **kwargs)
        max_image_size = 800
        print ('salvando...')
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)
        
    def get_preco_format(self):
        return utils.formata_preco(self.preco_marketing)

    def get_preco_promocional_format(self):
        return utils.formata_preco(self.preco_marketing_promocional)

    get_preco_format.short_description = 'Preço'
    
class Variacao (models.Model):
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
        
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name or self.produto.nome
    
    """
            Variacao:
            nome - char
            produto - FK Produto
            preco - Float
            preco_promocional - Float
            estoque - Int
    """