from django import forms # type: ignore 
from contact.models import Contact
from django.core.exceptions import ValidationError # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth import password_validation # type: ignore
from django.contrib.auth.models import User # type: ignore

# não precisa derivar uma classe de login, basta usar direto a classe AuthenticationForm
# class UserLoginForm(AuthenticationForm):
    
#     password = forms.CharField (
#         widget= forms.PasswordInput()
#     )
    
#     class Meta:
#         model = User
#         fields = (
#             'username', 'password'
#         )
    
#      # para validação dos campos do formulario:
#     def clean (self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')

#         print ('username', username)
#         print ('password', password)
        
#         if not User.objects.filter(username = username, password=password ).exists():
#             validation = ValidationError ('Usuário ou senha inválidos. Verifique!',code='invalid')
#             self.add_error ( 'username', validation)
#             self.add_error ( 'password', validation)
        
#         return super().clean()
    
class RegisterForm(UserCreationForm):
    
    email = forms.EmailField() # cria o campo html com a formatação especifica de endereço de email 
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2'
        )
    
    # para validar o campo email
    def clean_email (self):
        email = self.cleaned_data.get('email') 
        
        if User.objects.filter(email=email).exists():
            print ('email ja existe')
            self.add_error(
                'email',
                ValidationError('Este endereço de email ja esta em uso', 'invalid')
            )
        
        return email

class UpdateRegisterForm(forms.ModelForm):
    
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text= password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username'
        )
        
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False) # recupera o cadastro do usuario
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()
    
    # para validar o campo email
    def clean_email (self):
        email = self.cleaned_data.get('email') 
        
        if User.objects.filter(email=email).exists():
            print ('email ja existe')
            self.add_error(
                'email',
                ValidationError('Este endereço de email ja esta em uso', 'invalid')
            )
        
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1

class ContactForm (forms.ModelForm):
    
    picture = forms.ImageField(
        widget=forms.FileInput (
            attrs={
                'accept': 'image/*'
            }
        )
    )
    
    class Meta:
        model = Contact
        fields =  (
            'first_name',
            'last_name',
            'phone',
            'email', 'description', 'category', 'picture'
        )
        
    # para validação dos campos do formulario:
    def clean (self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        
        if first_name == last_name:
            validation = ValidationError ('O último nome informado não pode ser igual ao primeiro nome',code='invalid')
            self.add_error ( 'first_name', validation)
            self.add_error ( 'last_name', validation)
        
        return super().clean()
    
    # def clean_first_name(self):
    #     first_name = self.cleaned_data.get('first_name')
        
    #     if first_name == 'ABC':
    #         self.add_error (
    #             'first_name', 
    #             ValidationError (
    #                 'Não digite ABC neste campo!!!!!!',
    #                 code='invalid'
    #             )
    #         )
    #         # raise ValidationError('Não digite ABC neste campo', code='invalid')
            
    #     print ('passei no clean_first_name')
    #     return first_name