from decimal import Decimal
from django.conf import settings
from tienda.models import Producto


class Cart(object):
    
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID) 

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {} 

        self.cart = cart

    def add(self,producto,cantidad=1,override_cantidad=False):
        producto_id = str(producto.id)
        if producto_id not in self.cart:
            self.cart[producto_id] = {'cantidad':0,'precio':str(producto.precio)}
        
        if override_cantidad:
            self.cart[producto_id]['cantidad'] = cantidad
        else:
            self.cart[producto_id]['cantidad'] += cantidad
        self.save()
    
    def save(self):
        self.session.modified = True

    # metodo para eliminar un producto del carrito
    def remove(self,producto):
        producto_id = str(producto.id)

        if producto_id in self.cart:
            
            del self.cart[producto_id]
        self.save()

    # metodo para eliminar todo nuestro carrito
    def clear(self): 
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def __iter__(self): 
        producto_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        cart = self.cart.copy()

        for producto in productos:
            cart[str(producto.id)]['producto'] = producto
        
        for item in cart.values():
            item['precio'] = Decimal(item['precio'])
            item['precio_total'] = item['precio'] * item['cantidad']
            yield item
    
    #metodo para calcular el precio total de todos los productos del carrito
    def get_total_price(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values())
    
    def __len__(self):
       return sum(item['cantidad'] for item in self.cart.values()) 










    
    








