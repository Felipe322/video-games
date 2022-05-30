from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Videojuego
from .forms import CategoriaForm, VideojuegoForm
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.paginator import Paginator
from django_weasyprint import WeasyTemplateResponseMixin

from django.conf import settings
from .models import DetalleVenta, Venta


def lista_categoria(request):
    categorias = Categoria.objects.all()
    paginator = Paginator(categorias, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'lista_categorias.html', {'categorias': categorias, 'page_obj': page_obj})

def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('categoria:lista')

def nuevo_categoria(request):
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria:lista')
    context = {'form': form }
    return render(request, 'nuevo_categoria.html', context)

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria:lista')
    context = {'form': form }
    return render(request, 'editar_categoria.html', context)


class VideojuegoList(ListView):
    model = Videojuego
    paginate_by = 5

class VideojuegoEliminar(DeleteView):
    model = Videojuego
    success_url = reverse_lazy('videojuego:lista')

class VideojuegoCrear(CreateView):
    model = Videojuego
    form_class = VideojuegoForm
    extra_context = {'etiqueta': 'Nuevo','boton': 'Agregar',  'vj_nuevo':True}
    success_url = reverse_lazy('videojuego:lista')

class VideojuegoActualizar(UpdateView):
    model = Videojuego
    form_class = VideojuegoForm
    extra_context = {'etiqueta': 'Actualizar', 'boton': 'Guardar'}
    success_url = reverse_lazy('videojuego:lista')

class VideojuegoDetalle(DetailView):
    model = Videojuego

class Grafica(TemplateView):
    template_name = 'videojuego/grafica.html'
    
    def get(self, request, *args, **kwargs):
        videojuegos_categorias = Videojuego.objects.all().values('categoria').annotate(cuantos=Count('categoria'))
        categorias = Categoria.objects.all()

        datos = []
        for categoria in categorias:
            cuantos = 0
            for vc in videojuegos_categorias:
                if vc['categoria'] == categoria.id:
                    cuantos = vc['cuantos']
                    break
            datos.append({'name': categoria.nombre, 'data':[cuantos]})
        self.extra_context = {'datos': datos}
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class VistaPDF(ListView):
    model = Videojuego
    template_name = 'videojuego/videojuego_pdf.html'

class VideojuegoPDF(WeasyTemplateResponseMixin, VistaPDF):
    pdf_stylesheets = [
        settings.STATICFILES_DIRS[0] + 'css/portal.css',
    ]
    pdf_attachment = False
    pdf_filename = 'videojuegos.pdf'

class VistaPDFDetalle(DetailView):
    model = Videojuego
    template_name = 'videojuego/pdf_detalle.html'


class VideojuegoPDFDetalle(WeasyTemplateResponseMixin, VistaPDFDetalle):
    pdf_stylesheets = [
    settings.STATICFILES_DIRS[0] + 'css/portal.css',
    ]
    pdf_attachment = False
    pdf_filename = 'videojuego_detalle.pdf'


def resumen_compra(request):
    context = {}
    articulos = []
    total = 0.0
    for articulo in request.session['articulos']:

        precio = request.session['articulos']['precio']
        cantidad = request.session['articulos']['cantidad']
        articulo_nuevo = Videojuego.objects.get(id=articulo)

        articulos.append({'nombre':articulo_nuevo.titulo,
                           'precio':precio,
                           'cantidad':cantidad ,
                           'total':cantidad*precio
                            })
        total = total + (cantidad*precio)

    context = {'articulos': articulos,
               'total':total
              }
    return render(request, 'carito_compras.html',context)

def comprar(request):
    venta_nueva = Venta.objects.create( usuario='felipe322')
    if venta_nueva.is_valid():
        venta_nueva.save()
        #return redirect('categoria:lista')

    for articulo in request.session['articulos']:
        total_cantidad = request.session['articulos']['cantidad']
        articulo_nuevo = Videojuego.objects.get(id=articulo)
        detalle_venta = DetalleVenta.objects.create(
            cantidad = total_cantidad,
            venta = venta_nueva,
            videojuego = articulo_nuevo
        )
        detalle_venta.save()

    return redirect('videojuego:lista')