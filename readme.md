# Instalación

## Instalación de dependencias:

Suponiendo que tiene sqlite3 y python instalado en su ordenador:

- Si quisiera, cree un entorno virtual:
```
python -m venv venv
```

- En caso de haber creado el entorno virtual, acceda a él:
    + Windows: venv\Scripts\activate
    + Mac y Linux: . venv/bin/activate

- En caso de haber creado el entorno virtual, en el archivo '.env' definir las siguientes variables:
    + FLASK_APP=application.py
    + FLASK_ENV=development

- Ejecutar:
```
pip install -r requirements.txt
```

## Obtención API coinmarketcap:

- Diríjase a https://coinmarketcap.com/api/
- Obtenga su API Key

## Creación de la Base de datos:

- En el terminal, acceda a la carpeta data
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

- Ejecute python application.py