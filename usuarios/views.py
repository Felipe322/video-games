from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.views import generic
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .models import Usuario, Municipio, Estado
from .forms import UsuarioForm
from .token import token_activacion

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


class NuevoUsuario(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    extra_context = {'etiqueta': 'Nuevo', 'boton': 'Agregar'}
    success_url = reverse_lazy('usuarios:lista')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        dominio = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_activacion.make_token(user)
        mensaje = render_to_string('confirmar_cuenta.html',
            {
                'usuario': user,
                'dominio': dominio,
                'uid': uid,
                'token': token
            }
        )
        asunto = 'Activa cuenta Videojuegos'
        to = user.email
        email = EmailMessage(
            asunto,
            mensaje,
            to=[to]
        )
        email.content_subtype = 'html'
        email.send()


        return super().form_valid(form)

class UsuariosList(PermissionRequiredMixin, ListView):
    permission_required = 'videojuegos.view_usuarios'
    model = Usuario
    paginate_by = 5


class UsuarioActualizar(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    extra_context = {'etiqueta': 'Actualizar', 'boton': 'Guardar'}
    success_url = reverse_lazy('usuarios:lista')

    # def get_object(self, queryset=None):
    #     pk = self.request.user.pk
    #     obj = Usuario.objects.get(pk=pk)
    #     return obj

class UsuarioDetalle(LoginRequiredMixin, DetailView):
    model = Usuario

class UsuarioEliminar(LoginRequiredMixin, DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuarios:lista')

class LoginUsuario(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

class SingupUsuario(generic.CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('usuarios:login')

# class EditarPermisosGrupos(LoginRequiredMixin, UpdateView):
#     model = Usuario
#     success_url = reverse_lazy('usuarios:lista')
#     template_name  = 'editar_grupos.html'
#     def form_valid(self, form):
#         my_user = form.save()
#         if str(form).count('checked') == 0:
#             return redirect(reverse_lazy("usuario:lista"), {"alerta":"Elcoja mínimo un grupo."})

#         my_user = form.save()
#         return super().form_valid(form)

class ActivarCuenta(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs['uid64'])
            token = kwargs['token']
            user = Usuario.objects.get(id=uid)
        except:
            user = None

        if user and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(self.request, 'Cuenta activada con éxito')
        else:
            messages.error(self.request, 'Token inválido, contacta al administrador')

        return redirect('usuarios:login')

def obtiene_municipios(request):
    # estado = get_object_or_404(Estado, id=id_estado)
    if request.method == 'GET':
        return JsonResponse({'error':'Petición incorrecta'}, safe=False,  status=403)
    id_estado = request.POST.get('id')
    municipios = Municipio.objects.filter(estado_id=id_estado)
    json = []
    if not municipios:
        json.append({'error':'No se encontrar municipios para ese estado'})
        
    for municipio in municipios:
        json.append({'id':municipio.id, 'nombre':municipio.nombre})
    return JsonResponse(json, safe=False)