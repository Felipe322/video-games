import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videojuegos.settings')
django.setup()

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from videojuegos.usuarios.models import Usuario

administradores = Group.objects.create(name='administradores')
usuarios = Group.objects.create(name='usuarios')

content_type = ContentType.objects.get_for_model(Usuario)

permiso_usuarios = Permission.objects.create(
    codename = 'permiso_usuario',
    name = 'Permiso requerido para el grupo usuarios',
    content_type = content_type
)

permiso_administradores = Permission.objects.create(
    codename = 'permiso_administradores',
    name = 'Permiso requerido para el grupo administradores',
    content_type = content_type
)

usuarios.permissions.add(permiso_usuarios)
administradores.permissions.add(permiso_administradores)

administrador = Usuario.objects.create_user('your_email', password='your_password')
administrador.groups.add(administradores)

Usuario.objects.create_superuser('admin@admin.com', password='admin123')
