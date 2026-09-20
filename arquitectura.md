En este documento se describe la estructura y organización del sistema.

Este sistema está desarrollado bajo el patrón MVT propio de DJANGO, que es una adaptación del modelo MVC adaptado al desarrollo web.
Modelo: Gestiona la lógica de datos y reglas del negocio.
Vista: Contiene la lógica de control, interactúa con los modelos para obtener datos y decide qué plantilla mostrar
Plantilla: Contiene la interfaz con la cual interactúa el usuario.

Directorio del proyecto:
📁 taller_mecanico/            # Carpeta raíz del sistema
 │
 ├── 📁 core/                   # Configuración del proyecto 
 │    ├── settings.py           # Configuración general (BD, seguridad, apps)
 │    └── urls.py               # Enrutador principal de direcciones web

 │
 ├── 📁 static/                 # Archivos estáticos globales como estilos CSS
 ├── 📁 templates/              # Vistas en HTML5
 ├── manage.py                  # Archivo ejecutable de comandos de Django
 └── README.md                  # Presentación general del proyecto y su configuración


Comunicación con el exterior y flujo de datos:
El sistema web se comunica con el exterior siguiendo el protocolo estándar HTTP/HTTPS bajo el modelo cliente-servidor

Petición: El usuario realiza una acción en el navegador lo cual envía una petición HTTP hacia el servidor de Django.
Enrutamiento: El archivo `urls.py` recibe la petición y la deriva a la Vista (`views.py`) correspondiente.
Lógica y datos: La Vista solicita los datos necesarios al Modelo (`models.py`), el cual realiza una consulta a la base de datos.
Respuesta: El Modelo devuelve los datos a la Vista, esta los inyecta en la Plantilla HTML (`templates/`) y el servidor envía la página al navegador del usuario.
Interactividad: En el navegador, el código JavaScript se encarga de procesar alertas rápidas o validaciones sin necesidad de recargar la página completa.
