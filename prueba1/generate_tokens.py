import os
import django

# Set up the Django settings module for the script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prueba1.settings')  # Replace 'prueba1' with your project name
django.setup()

from rest_framework.authtoken.models import Token
from apptest.models import Usuario  # Replace with your app name and model if necessary

# Now you can access models and perform the actions
users = Usuario.objects.all()

for user in users:
    token, created = Token.objects.get_or_create(user=user)
    print(f"Token for {user.email}: {token.key}")