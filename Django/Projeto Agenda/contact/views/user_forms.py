from django.shortcuts import render, redirect # type: ignore
from contact.forms import RegisterForm, UpdateRegisterForm #UserLoginForm
from django.contrib import auth, messages # type: ignore
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore

# Create your views here.
def user_login (request):
       
    form = AuthenticationForm() #UserLoginForm()
    
    print ('method', request.method)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)    
        
        if form.is_valid() :
            user = form.get_user()
            print('User: ', user)
            
            # A variavel "user" é armazenada para uso eventual
            auth.login(request, user) #faz a autenticação do usuario (efetiva o login)
            messages.success(request, 'Usuário Logado!')
            return redirect('contact:index')
        else:
            messages.error(request, 'Login inválido!')
            
    return render(
        request, 'user/login.html', context= {
            'form': form,
            'form_title': 'Login'
        }
    )

@login_required(login_url='contact:user_login')
def user_logout (request):
       
    print ('method', request.method)
            
    # A variavel "user" é armazenada para uso eventual
    auth.logout(request) 
    messages.info(request, 'Usuário Desconectado!')
    return redirect('contact:user_login')

@login_required(login_url='contact:user_login')
def user_update(request):
    
    user = auth.get_user(request)
    
    if not user.is_authenticated:
        messages.warning(request, "Não há usuário logado. É necessário efetuar o login no sistema")
        return redirect('contact:user_login')
      
    form = UpdateRegisterForm(instance=request.user) # carrega o formulario com os dados do usuario
    
    if request.method == 'POST':
        form = UpdateRegisterForm (request.POST, instance=request.user)    
        
        if form.is_valid() :
            form.save()
            messages.success(request, 'Usuário alterado!')
            return redirect('contact:index')
    
    return render(
        request, 'user/register.html', context= {
            'form': form,
            'form_title': 'Update'
        }
    )
    
    
def register(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)    
        
        if form.is_valid() :
            form.save()
            messages.success(request, 'Usuário registrado!')
            return redirect('contact:user_login')
    
    return render(
        request, 'user/register.html', context= {
            'form': form,
            'form_title': 'Register'
        }
    )
    
   