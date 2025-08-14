#!/usr/bin/env python3
"""
Script para iniciar la aplicación web EcoAnalyzer
Migración del proyecto tkinter original a Flask
"""

import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    try:
        import flask
        print("✅ Flask está instalado")
        return True
    except ImportError:
        print("❌ Flask no está instalado")
        print("Instalando dependencias...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        return True

def open_browser():
    """Abrir el navegador después de un delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:8081')
    print("🌐 Navegador abierto en http://localhost:8081")

def main():
    print("🌱 EcoAnalyzer Web - Iniciando aplicación...")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ Error instalando dependencias")
        return
    
    # Programar apertura del navegador
    timer = Timer(2.0, open_browser)
    timer.start()
    
    print("🚀 Iniciando servidor Flask en puerto 8081...")
    print("📊 Accede a tu aplicación en: http://localhost:8081")
    print("🔐 Credenciales por defecto: admin / 1234")
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    # Iniciar la aplicación
    try:
        from web_app import app, init_databases
        init_databases()
        app.run(debug=False, host='0.0.0.0', port=8081)
    except KeyboardInterrupt:
        print("\n⏹️  Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando la aplicación: {e}")

if __name__ == '__main__':
    main()