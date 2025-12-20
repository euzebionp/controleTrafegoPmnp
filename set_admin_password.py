import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    user.set_password('14082025')
    user.save()
    print('✅ Senha do usuário admin atualizada para: 14082025')
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'olivertinoborges.euzebio@gmail.com', '14082025')
    print('✅ Superusuário admin criado com senha: 14082025')
