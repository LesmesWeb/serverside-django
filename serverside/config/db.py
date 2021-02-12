import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LOCAL_CAMILO = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db', #clarity_produccion_migrado 
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost', #IP de su equipo, no publica
        'PORT':  '5432',
	}
}
