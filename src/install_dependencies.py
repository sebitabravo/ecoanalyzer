import importlib
import subprocess

# Lista de módulos a comprobar
modulos = ['Pillow', 'customtkinter', 'matplotlib']


def comprobar_instalacion(modulo):
    try:
        importlib.import_module(modulo)
        return True
    except ImportError:
        return False


def instalar_modulo(modulo):
    subprocess.run(['pip', 'install', modulo])


if __name__ == "__main__":
    # Comprobación e instalación de módulos faltantes
    for modulo in modulos:
        if not comprobar_instalacion(modulo):
            instalar_modulo(modulo)
