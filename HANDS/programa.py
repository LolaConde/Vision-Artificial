import tkinter as tk

# Programa creado con ChatGPT. Crea una ventana con el título "Programa abierto por mano.py".
# Si se ejecuta este programa, se abre una ventana, y si se deja de ejecutar, se cierra la ventana.

def main():
    # Crear la ventana
    ventana = tk.Tk()
    
    # Configurar el título de la ventana
    ventana.title("Programa abierto por mano.py")

    # Configurar las dimensiones de la ventana
    ventana.geometry("400x200")

    # Ejecutar el bucle principal de la aplicación
    ventana.mainloop()

if __name__ == "__main__":
    main()
