# Api Sinonimos

* En este proyecto se desarrolla una aplicación para procesamiento de igredientes medicos.

### Configuración 🔧

* Crea un ambiente virtual con la version 3.8 de python. 
* Instala los paquetes necesarios ubicados en el archivo requirements.txt

```
pip install -r requirements.txt
```
* Configure los parametros de la base de datos en el archivo medicalapi/processor/api_processor.py

HOST = servidor
USER = usuario de la base de datos
DBPASS = contraseña de la base de datos
DBNAME = nombre de la base de datos

* crea una base de datos mysql con un nombre a su gusto y corre el archivo script.txt en la bd.

## Ejecutando el proyecto ⚙️

* Corre el proyecto con el comando python manage.py runserver

```
 python manage.py runserver
```
* Ahora invoca el endpoint http://localhost:8000/apicall/ para ejecutar el proceso de consumo de los ingredientes. Lo puedes hacer desde el navegador o con postman.

Eso es todo, puedes apreciar los resultados en la base de datos.

Proyecto hecho con ❤️
