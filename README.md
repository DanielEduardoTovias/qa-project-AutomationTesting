## PROYECTO. Pruebas automatizadas para la aplicación "Urban Routes" con Python y Selenium
     Descripción:
    - En este proyecto se realizaron pruebas automatizadas para la aplicación Urban Routes en las cuales se abarcan los escenarios de pedir un automóvil y agregar ciertas configuraciones al pedido del transporte realizando las pruebas con Python y Selenium y algunas librerías extras con el patrón de diseño POM (Page Object Model).
    

## Pasos para ejecutar las pruebas automatizadas:
- Iniciar el servidor y copiar la URL (Dirección ): en la variable urban_routes_url en el script: "data.py"
- En el script "main.py", ejecutar los testScripts que están en la clase: "class TestUrbanRoutes"
- Ejecutar individualmente cada testScript haciendo clic en el símbolo "play" a la izquierda de la función y seleccionando la opción "Run..."
- Ejecutar todos los testScripts haciendo clic en el símbolo "play" a la izquierda de la clase:
"class TestUrbanRoutes:" y selecionar la opción "Run..."


## Escenarios que abarcan las pruebas automatiadas:
1.  Configurar la dirección.
2.  Seleccionar la tarifa Comfort.
3.  Rellenar el número de teléfono.
4.  Agregar una tarjeta de crédito.
5.  Escribir un mensaje para el controlador.
6.  Pedir una manta y pañuelos.
7.  Pedir 2 helados.
8.  Aparce el modal para buscar un taxi.
9.  Validar que aparezca el número de automóvil n la información espués de pedir el automóvil

## Sobre el script data.py:
El script data.py contiene variables que se utilizarán para los campos de entra de las pruebas automatizadas junto con la URL del servidor que se inserta cuando se inicia o reinicia el mismo.

## Sobre el script main.py:
Están las librerías que se utilizarán en el script y está también (import data) que es la clase antes mencionada para poder obtener las variables a usar.

Hay una función (def retrieve_phone_code(driver) -> str:) que sirve para regresar un codigo que se ingresa en un campo de entrada una vez ingresado el número de teléfono en el punto 3 función (def add_phone_number(self, phone_number):).

Enseguida está la clase: class UrbanRoutesPage:
donde se encuentran los atributos y métodos [definidos por las acciones a abarcar] (localizadores y acciones) de la aplicación que, posteriormente esas funciones, se utilizarán en los tests y los atributos para poder localizar los elementos en la aplicación.

Ya al final está la clase que contiene los testScripts con dos métodos de clase [que sólo se utilizan en esa clase y que se ejecutan  una vez antes y después de cada test] @classmethod 
(   def setup_class(cls): y def teardown_class(cls):   ).

los casos de prueba automatizados son funciones que empiezan con la palabra "test" seguido del nombre de la acción o acciones haiendo alusión a lo que se realizará en ese testScript





