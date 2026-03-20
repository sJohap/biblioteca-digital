"""
Este archivo es el punto de entrada de la aplicación de gestión de libros.

Funciones principales:
- Inicializa la base de datos si no existe.
- Verifica la conexión a SQLite y muestra un mensaje de error si falla.
- Crea la ventana principal con Tkinter y aplica el tema "arc" (ttkthemes).
- Ejecuta la clase LibrosApp que contiene la lógica de la interfaz gráfica.
"""
from tkinter import messagebox
from ttkthemes import ThemedTk

from conexion_gui import get_connection, init_db
from gui_libros import LibrosApp

# Crear la base si no existe
init_db()

def main():
    conn = get_connection()
    if not conn:
        messagebox.showerror("❌ Error de Conexión", 
                           "No se pudo conectar a la base de datos.\n\n"
                           "Verifique que SQLite esté funcionando correctamente.")
        return
    conn.close()

    # Crear y ejecutar la aplicación
    root = ThemedTk(theme="arc")
    app = LibrosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
