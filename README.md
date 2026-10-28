# Convertidor de Excel a DBF

Aplicación gráfica desarrollada en Python para convertir archivos de Excel
(`.xlsx` o `.xls`) a formato DBF. El programa permite seleccionar el archivo
desde una ventana, genera automáticamente la estructura de la tabla DBF y
guarda el resultado en la misma carpeta del archivo de Excel.

## Requisitos

- Python 3.9 o superior
- `pandas`
- `dbf`
- `PyQt6`
- `openpyxl` para archivos `.xlsx`
- `xlrd` para archivos `.xls`

## Instalación

Se recomienda utilizar un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual:

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
python -m pip install pandas dbf PyQt6 openpyxl xlrd
```

## Ejecución

Desde la carpeta del proyecto, ejecutar:

```bash
python convertidor_zonas_ho.py
```

También se puede usar el ejecutable de Python del entorno virtual:

```bash
.venv/bin/python convertidor_zonas_ho.py
```

## Uso de la aplicación

1. Ejecutar el programa.
2. Presionar **Seleccionar Archivo**.
3. Elegir un archivo Excel con extensión `.xlsx` o `.xls`.
4. Presionar **Convertir a DBF**.
5. Esperar a que la barra de progreso llegue al 100 %.
6. El archivo DBF se creará en la misma ubicación y con el mismo nombre base
   que el archivo Excel.

Por ejemplo:

```text
zonas_ho_Puntarenas.xlsx
zonas_ho_Puntarenas.dbf
```

## Conversión de tipos de datos

El esquema DBF se genera a partir de los tipos de datos detectados en cada
columna del archivo Excel:

| Tipo detectado en Excel | Tipo DBF |
| --- | --- |
| Entero | `N(18,0)` |
| Decimal | `N(18,5)` |
| Fecha y hora | `D` |
| Booleano | `L` |
| Texto u otro tipo | `C(250)` |

## Reglas aplicadas a las columnas

- Los espacios y guiones de los nombres de columnas se reemplazan por
  guiones bajos.
- Los nombres de columnas se limitan a 10 caracteres, debido a la
  especificación tradicional del formato DBF.
- Los valores de texto se limitan a 250 caracteres.
- Las celdas vacías se guardan como valores nulos.
- El archivo DBF se crea usando la codificación `cp1252`, compatible con
  caracteres como tildes y la letra `ñ`.

## Estructura del proyecto

```text
.
├── convertidor_zonas_ho.py       # Aplicación de conversión
├── zonas_ho_Puntarenas.xlsx      # Ejemplo de archivo de entrada
├── zonas_ho_Puntarenas.dbf       # Ejemplo de archivo convertido
└── README.md                     # Documentación del proyecto
```

## Consideraciones

- Si ya existe un DBF con el mismo nombre, puede ser reemplazado al ejecutar
  una nueva conversión.
- Los nombres de columnas que queden iguales después de limitarse a 10
  caracteres pueden producir conflictos en el esquema DBF; se recomienda
  revisar los encabezados del Excel antes de convertirlo.
- Las columnas de texto se truncan a 250 caracteres para ajustarse al
  esquema generado.
- El programa muestra un mensaje de éxito o de error al finalizar la
  conversión.

## Tecnologías utilizadas

- **Python**
- **PyQt6** para la interfaz gráfica
- **pandas** para leer y procesar archivos Excel
- **dbf** para crear y escribir archivos DBF
