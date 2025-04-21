# trabajo_S4_wiki_tf
 wiki the forest en django


para poder ejecutar: 



crear ambiente python

ingresar 
pip install -r requirements.txt.

cambiar dirección de Base de Datos oracle sql en Settings.py

python manage.py makemigrations
python manage.py migrate.

python manage.py createsuperuser


entrar a http://127.0.0.1:8000/admin/socialaccount/socialapp/ y añadir:

nombre:google
id:340007672691-1bgm2aq28kv4dhcl6ef72t0nj0m5bmh6.apps.googleusercontent.com
secret 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
sites: añadir localhost a sitios elegidos.



para utilizar la api rest

url:http://127.0.0.1:8000/usuario/<email>/

<email> = dirección email que se quiere consultar.

la respuesta muesta información del usuario si es que existe en la DB.
