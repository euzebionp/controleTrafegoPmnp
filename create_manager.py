import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create a new superuser 'manager'
try:
    user = User.objects.get(username='manager')
    user.delete()
    print('Usuário manager existente removido.')
except User.DoesNotExist:
    pass

user = User.objects.create_superuser('manager', 'manager@example.com', 'manager123')
print('✅ Novo superusuário criado: manager / manager123')
