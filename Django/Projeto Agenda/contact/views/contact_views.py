from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.db.models import Q # type: ignore
from contact.models import Contact
from django.core.paginator import Paginator # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore

# Create your views here.

@login_required(login_url='contact:user_login')
def index (request):
    
    contacts = Contact.objects.filter(show=True, owner=request.user).order_by('-id')
    
    paginator = Paginator(contacts,7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    context = {
        'contacts' : page_obj.object_list,
        'site_title': 'Contatos - ',
        'page_obj': page_obj
    }
    return render(
        request, 'contact/index.html', context= context
    )
    
@login_required(login_url='contact:user_login')   
def search (request):
    
    print ('search...')
    
    search_value = request.GET.get('q', '').strip()
    print('search_value: ', search_value)
    
    if (search_value == ""):
        return redirect("contact:index")
    
    contacts = Contact.objects.filter(show=True, owner=request.user)\
            .filter(
                Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value) # permite usar OR para pesquisar outro campo usando | combinada com a função Q
                )\
            .order_by('-id')
    
    paginator = Paginator(contacts,7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'contacts' : page_obj.object_list,
        'site_title': 'Contatos - ',
        'search_value': search_value,
        'page_obj' :page_obj
    }
    return render(
        request, 'contact/index.html', context= context
    )

@login_required(login_url='contact:user_login')
def contact (request, id):
    
    print ("id=", id)
    
    contact = get_object_or_404(Contact, pk=id, show=True, owner=request.user)
    #contact = Contact.objects.filter(id=id, show=True, owner=request.user).first()
    
    contact_name = f'{contact.first_name} {contact.last_name} - '

    context = {
        'contact' : contact,
        'site_title': contact_name
    }
    
    return render(
        request, 'contact/contact.html', context = context
    )