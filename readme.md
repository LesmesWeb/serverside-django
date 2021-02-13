# ServerSide Implementado

levantar servidor con:
- $ python manage.py runserver 0:8001

user admin
- Usuario: admin@admin.com
- Contraseña: 123

## Convenciones necesarias:

- Todo en español o todo en ingles.
- Variables de entorno en el config de Django.
- Lo que hacen las clases o librerias debe ponerse en la documentación y evitar dejarlo en el codigo.

### Django:
0. Variable en              : Minúscula o snake_case
1. Clases en                : Uppercamel (ListaRegla)
2. Name de las urls en      : snake_case (lista_regla)
3. Importaciones de la siguiente manera
    - import (import json)
    - libreria del framework django (django.urls import reverse_lazy)
    - Apps y herencias  (apps.proyecto.views import _FormValid)
    - importaciones propias del app como formularios, modelos y filters (.forms import ActorForm)

### JavaScript:
0. Variable en              : Minúscula o snake_case
1. Funciones en            : Camelcase (mostrarErrorCreacionForm)
