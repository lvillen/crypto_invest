# Instalación

En esta guía asumimos que las llamadas a python en terminal se hacen como 'python'. En caso de que python3 no este renombrado como python, tenga en cuenta que tendrá que hacerlo como 'python3'

## Instalación de dependencias:

Suponiendo que tiene python y los módulos sqlite3 y venv instalados en su ordenador:

- Si quisiera, cree un entorno virtual, acceda al terminal e introduzca:
    ```
    python -m venv venv
    ```

- En caso de haber creado el entorno virtual, acceda a él vía terminal:
    + Windows: venv\Scripts\activate
    + Mac y Linux: . venv/bin/activate

- En caso de haber creado el entorno virtual, cree, a nivel raíz, el archivo '.env' y defina las siguientes variables:
    + FLASK_APP=application.py
    + FLASK_ENV=development

- Ejecutar en el terminal:
    ```
    pip install -r requirements.txt
    ```

## Obtención API coinmarketcap:

- Diríjase a https://coinmarketcap.com/api/
- Obtenga su API Key

## Creación de la Base de datos:

- En el terminal, acceda a la carpeta data.
- Ejecutar:
    ```
    python initdb.py
    ```

## Fichero de configuración:

- Renombre su config_template.py como config.py.
- Introduzca una clave secreta.
- Introduzca la API KEY obtenida.
- Introduzca la ruta a la base de datos.

## Ejecución:

- En el terminal, vuelva a la carpeta raíz y ejecute python application.py