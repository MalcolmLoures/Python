from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.db.models import Q # type: ignore
from django.core.paginator import Paginator # type: ignore
from contact.forms import ContactForm
from django.urls import reverse # type: ignore
from contact.models import Contact
from django.contrib.auth.decorators import login_required # type: ignore

# Create your views here.
@login_required(login_url='contact:user_login')
def create (request):

    form_action = reverse('contact:create') # para identificar a url
    
    print (form_action)
    print ('request.method =', request.method)
    
    if request.method == "POST":  
        form = ContactForm(data=request.POST, files=request.FILES)
        context = {
            'form': form,
            'form_action': form_action
        }
        
        if form.is_valid():
            contact = form.save(commit=False) # false, usando so para recuperar os dados sem salvar efetivamente na base de dados
            contact.owner = request.user # atribui o usuario owner do registro
            contact.save()
                        
            print (contact, contact.id)
            return redirect ('contact:update', contact_id=contact.id)
        else:
            print ('formulário é INvalido!')
            
    
        return render(
            request, 'contact/create.html', context= context
        )
    
    context  =  {
        'form': ContactForm(),
        'form_action': form_action
    }
    
    return render (
        request, 'contact/create.html', context=context
    )

@login_required(login_url='contact:user_login')
def update (request,contact_id):
    
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
    
    print ('achei contact:', contact)
    form_action = reverse('contact:update', args=(contact_id,)) # monta a url para compor o action do formulario
    
    print (form_action)
    print ('request.method =', request.method)
    
    if request.method == "POST":  
        form = ContactForm(data=request.POST, instance=contact, files=request.FILES)
        context = {
            'form': form,
            'form_action': form_action
        }
        
        if form.is_valid():
            contact = form.save()
            return redirect ('contact:update', contact_id=contact.id)
        else:
            print ('formulário é INvalido!')
            
    
        return render(
            request, 'contact/create.html', context= context
        )
    
    context  =  {
        'form': ContactForm(instance=contact),
        'form_action': form_action
    }
    
    return render (
        request, 'contact/create.html', context=context
    )
    
@login_required(login_url='contact:user_login')
def delete (request,contact_id):
    
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
    
    confirmation = request.POST.get('confirmation', 'no')
    
    print ('achei contact:', contact)    
    print ('request.method =', request.method)
    
    if confirmation == 'yes':
        contact.delete()
        return redirect ('contact:index')
    
    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation
        }
    )    
    