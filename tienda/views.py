from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from .forms import RegisterForm,ProductoForm
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from cart.cart import Cart

# Create your views here.
def index(request):
    
    tresProductos = Producto.objects.all().order_by('-id')[:3]
    restoProductos = Producto.objects.all().order_by('-id')[3:10]
    categorias = Categoria.objects.all()
    return render(request,'index.html',{
        'title':'Jaguarete Kaa - Home',
        'tresProductos':tresProductos,
        'restoProductos':restoProductos,
        'categorias':categorias
    })

def acerca(request):
    categorias = Categoria.objects.all()
    return render(request,'acerca.html',{
        'title':'Sobre Nosotros',
        'categorias':categorias
    })

def login_view(request):
    
    if not request.user.is_authenticated: 
        categorias = Categoria.objects.all()
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(username=username,password=password)

            if user:
                login(request,user)
                messages.success(request,'Bienvenido a Jaguarete Kaa {}'.format(user.username))
                return redirect('tienda:index')
            else:
                messages.error(request, 'Usuario y/o contaseña no validos, intente nuevamente')

        return render(request,'tienda/users/login.html',{
            'categorias':categorias
        })
    return redirect('tienda:index')

def logout_view(request):
    if request.user.is_authenticated: 
        logout(request)
        messages.success(request,'Sesión cerrada correctamente')
        return redirect('tienda:index')

    return redirect('tienda:index')

def register(request):
    categorias = Categoria.objects.all()
    if request.user.is_authenticated:
        return redirect('tienda:index')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
         
        user = form.save()
        if user:
            login(request,user)
            messages.success(request,'Usuario creado exitosamente!')
            return redirect('tienda:index')
        
    return render(request,'tienda/users/register.html',{
        'form':form,
        'categorias':categorias
    })

def ver_producto(request,producto_id):
    
    producto = get_object_or_404(Producto,id=producto_id)
    categorias = Categoria.objects.all()


    if request.method == 'GET' and request.GET.get('cantidad'):
        cart = Cart(request)
        cart.add(producto,int(request.GET.get('cantidad')))

        messages.success(request,'Producto agregado exitosamente al carrito!')
        return redirect('tienda:index')
    elif not request.user.is_authenticated:
        return redirect('tienda:login')

    return render(request,'productos/ver_producto.html',{
        'producto':producto,
        'categorias': categorias,
    })

def producto_categoria(request,categoria_id):
    categoria = Categoria.objects.get(pk=categoria_id)
    categorias = Categoria.objects.all()
    productos = Producto.objects.all().filter(categoria=categoria)
    titulo = categoria.descripcion
    
    return render(request,'productos/categoria.html',{
        'categoria':categoria,
        'categorias':categorias,
        'productos': productos,
        'titulo':titulo
    })

class BuscarProductoListView(ListView):
    template_name = 'productos/buscar.html'
    
    def query(self):
        return self.request.GET.get('q')

    def get_queryset(self):
        return Producto.objects.filter(descripcion__icontains=self.query())
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['producto_list'].count()
        context['categorias'] = Categoria.objects.all() 
        return context

@login_required(login_url='usuarios/login')
def cargar_producto(request):
    
    if request.user.is_staff: 
        categorias = Categoria.objects.all()

        form = ProductoForm(request.POST, request.FILES)
        
        if request.method == 'POST' and form.is_valid():
        
            producto = form.save()
            if producto:
                messages.success(request,'Producto cargado exitosamente!')
                return redirect('tienda:nuevo')
            
        return render(request,'productos/nuevo_producto.html',{
            'form':form,
            'categorias':categorias
        })
    return redirect('tienda:index')

@login_required(login_url='usuarios/login')
def editar_producto(request,producto_id):

    if request.user.is_staff:
        un_producto = get_object_or_404(Producto,id=producto_id)
        categorias = Categoria.objects.all()
        if request.method == 'POST':
            form = ProductoForm(data=request.POST,files=request.FILES,instance=un_producto)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.GET['next'])
        else:
            form = ProductoForm(instance=un_producto)
            return render(request,'productos/modificar_producto.html',{
                'producto':un_producto,
                'form': form,
                'categorias':categorias
                
            })
    return redirect('tienda:index')

@login_required(login_url='usuarios/login')
def eliminar_producto(request,producto_id):
    if request.user.is_staff:
        un_producto = get_object_or_404(Producto,id=producto_id)
        un_producto.delete()
    messages.success(request,'Producto eliminado exitosamente!')
    return redirect('tienda:index')    

@login_required(login_url='usuarios/login')
def cart_detalle(request):
    categorias = Categoria.objects.all()
    return render(request,'cart/detail.html',{
        'cart':Cart(request),
        'categorias':categorias
    })

def cart_remove(request,pk):
    cart = Cart(request)
    producto = get_object_or_404(Producto,pk=pk)
    cart.remove(producto)
    return redirect('tienda:cart_detalle')

def cart_delete(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request,'¡Carrito vaciado con éxito, lo invitamos a seguir buscando!')
    return redirect('tienda:index')
