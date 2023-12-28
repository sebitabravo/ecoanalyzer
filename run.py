import subprocess
import os

if __name__ == "__main__":
    # Ejecutar install_dependencies.py
    ruta_install = os.path.join('src', 'install_dependencies.py')
    subprocess.run(['python', ruta_install])

    # Ejecutar login_screen.py
    ruta_login = os.path.join('src', 'login_screen.py')
    subprocess.run(['python', ruta_login])
