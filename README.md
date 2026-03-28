# PyLock CLI - Password Manager

PyLock CLI es un gestor de contraseñas ligero y robusto desarrollado en Python, diseñado para ejecutarse desde la terminal en entornos Linux. El sistema implementa estándares de cifrado simétrico para garantizar la integridad y confidencialidad de las credenciales almacenadas localmente.

## Caracteristicas Principales

* Cifrado AES-256: Implementado mediante la libreria cryptography (Fernet) para asegurar que los datos en disco permanezcan ilegibles sin la llave maestra.
* Seguridad por Hash: Validacion de acceso mediante el algoritmo SHA-256 para la Master Password.
* Generador de Entropia: Creacion de contraseñas aleatorias seguras utilizando el modulo secrets de Python (CSPRNG).
* Interfaz de Usuario: Consola organizada y estructurada mediante la libreria rich.
* Gestion de Datos: Funciones integradas para añadir, listar, generar y eliminar registros de forma eficiente.

## Requisitos del Sistema

* Python 3.x
* Fedora Linux o distribuciones basadas en Unix
* Dependencias: cryptography, rich

## Instalacion y Ejecucion

1. Clonar el repositorio:
   git clone https://github.com/Robles42/Gestor-de-Contrase-as-CLI-en-Python.git
   cd Gestor-de-Contrase-as-CLI-en-Python

2. Configurar el entorno virtual:
   python3 -m venv venv
   source venv/bin/activate
   pip install cryptography rich

3. Iniciar la aplicacion:
   python3 gestor.py

## Seguridad y Persistencia

El sistema genera tres archivos criticos a nivel local que estan protegidos mediante el archivo .gitignore para evitar su exposicion en repositorios publicos:

* master.key: Llave simetrica necesaria para el descifrado de datos.
* passwords.dat: Base de datos con las credenciales cifradas.
* master.hash: Verificador de integridad de la contraseña maestra.

Se recomienda mantener una copia de seguridad externa del archivo master.key, ya que su perdida imposibilita la recuperacion de los datos.

## Autor
Carlos Santiago Sanchez Robles - GitHub: Robles42
