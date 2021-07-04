from django import forms

from django.contrib import admin

#importamos model User
from django.contrib.auth.models import User
from .models import Producto,Categoria

class RegisterForm(forms.Form):
    
    username = forms.CharField(required=True,min_length=4,max_length=50,label='Usuario',
                widget=forms.TextInput(attrs={
                    'class':'form-control',
                    'id':'username',
                    'placeholder':'Ingrese nombre de usuario'
                })
            )
    email = forms.EmailField(required=True,label='Correo electrónico',
                widget=forms.EmailInput(attrs={
                    'class':'form-control',
                    'id':'email',
                    'placeholder':'example@jaguarete.com"'
                })
            )
    password = forms.CharField(required=True,label='Contraseña',
               widget=forms.PasswordInput(attrs={
                    'class':'form-control',
                    'id':'password',
                    'placeholder':'Ingrese una contraseña'
                }) 
            )
    password2 = forms.CharField(required=True,label='Confirmar contraseña',
               widget=forms.PasswordInput(attrs={
                    'class':'form-control',
                    'id':'password',
                    'placeholder':'Ingrese una contraseña'
                }) 
            )
    #validamos campo username, para que no existan usuarios repetidos
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya existe!')
        
        #si el usuario no existe, lo retornamos
        return username
    
    #validamos el campo email, para que  no registrar el mismo correo
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electrónico ya se encuentra registrado!')
        #si el correo no esta registrado, lo retornamos
        return email    
    
    #sobreescribimos el metodo clean, es decir, no vamos a crear otra funcion clean_password2
    #lo usamos solo si necesitamos validar campos que dependan de otros
    def clean(self):
        #obtenemos todos los datos del formulario
        cleaned_data = super().clean()

        #validamos
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            #utilizamos el metodo add_error para mostrar el error
            #necesitamos 2 parametros (1-campo al cual agregamos error y 2-texto del error)
            self.add_error('password2','Las contraseñas no coinciden')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )


class ProductoForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        fields =['titulo','imagen','descripcion','precio','categoria']
        widgets = {
            'titulo':forms.TextInput(attrs={
                'class':'form-control mb-3',
                'id':'titulo',
                'placeholder':'Ingrese nombre del producto',
            }),
            'imagen':forms.FileInput(attrs={
                'accept':'image/*',
                'class': 'form-control mb-3'    
            }),
            'descripcion':forms.Textarea(attrs={
                'class':'form-control mb-3',
                'id':'descripcion',
                'placeholder':'Ingrese descripción del producto',    
            }),
            'precio':forms.NumberInput(attrs={
                'class':'form-control mb-3',
                'id':'precio',
                'placeholder':'$XXX.XX',
                'min':0
            }),
            'categoria':forms.Select(attrs={
                'class':'form-control mb-3'
            })
            
        }
        
   