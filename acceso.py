import os
from win32com.client import Dispatch

def crear_acceso_directo():
    # Ruta al escritorio del usuario
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Ejecutable de Python (pythonw.exe evita la consola negra)
    path_python = r"C:\Python313\pythonw.exe"
    
    # Ruta de tu script
    path_script = r"C:\Users\Pablo\Desktop\Programa genera cuadros en ingles\nuevo-programa-creador-pdf-modificado\programa_genera_pdf.py"
    
    # Ruta del ícono (puede estar en la misma carpeta del script)
    path_icono = r"C:\Users\Pablo\Desktop\Programa genera cuadros en ingles\nuevo-programa-creador-pdf-modificado\cronus.ico"
    
    # Nombre y ruta del acceso directo que se creará
    path_acceso_directo = os.path.join(escritorio, "Generador de PDF.lnk")

    # Crear el acceso directo
    shell = Dispatch('WScript.Shell')
    acceso_directo = shell.CreateShortCut(path_acceso_directo)
    acceso_directo.Targetpath = path_python
    acceso_directo.Arguments = f'"{path_script}"'
    acceso_directo.WorkingDirectory = os.path.dirname(path_script)
    acceso_directo.IconLocation = path_icono
    acceso_directo.save()

    print("✅ Acceso directo creado en el escritorio correctamente.")

crear_acceso_directo()
