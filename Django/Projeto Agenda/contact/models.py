from django.db import models # type: ignore
from django.utils import timezone # type: ignore
from django.contrib.auth.models import User

# Create your models here.

class Category (models.Model):
  class Meta:
      verbose_name = 'Categoria'
      verbose_name_plural = 'Categorias'
      
  name = models.CharField(max_length=50)
  def __str__(self):
     return self.name

class Contact (models.Model):
    class Meta:
      verbose_name = 'Contato'
      verbose_name_plural = 'Contatos'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField( blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')
    category = models.ForeignKey(Category, 
                                  on_delete=models.SET_NULL,
                                  blank=True, null=True
                                )
    owner = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                blank=True, null=True
                              )
    def __str__(self):
        return f'{self.first_name} {self.last_name}'  # usado para mostrar o registro la lista de consulta
    
