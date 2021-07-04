from django.db import models

class Categoria(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Producto(models.Model):
    titulo = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="productos/%Y/%m/%d")
    descripcion = models.TextField()
    precio = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="categoria_producto")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

