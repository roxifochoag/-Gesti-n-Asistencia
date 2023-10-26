import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

# Conectar a la base de datos SQLite
conn = sqlite3.connect("alumnos.db")
cursor = conn.cursor()

# Crear una tabla para almacenar los datos de los alumnos
cursor.execute('''CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    apellido TEXT,
    codigo TEXT,
    rostro BLOB
)''')
conn.commit()

class Alumno:
    def __init__(self, nombre,apellido, codigo):
        self.nombre = nombre
        self.codigo = codigo
        self.apellido = apellido
        self.rostro = None

# Función para registrar un alumno en la base de datos
def registrar_alumno():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    codigo = codigo_entry.get()
    if not nombre or not codigo or not apellido:
        messagebox.showerror("Error", "Ingresa el nombre, apellido y el código del alumno.")
        return

    alumno.nombre = nombre
    alumno.codigo = codigo
    alumno.apellido = apellido
    

    cursor.execute("INSERT INTO alumnos (nombre, codigo,apellido, rostro) VALUES (?,?, ?, ?)",
                   (alumno.nombre, alumno.codigo, alumno.rostro,alumno.apellido))
    conn.commit()
    messagebox.showinfo("Éxito", "Alumno registrado con éxito")

# Función para capturar el rostro de un alumno
def capturar_rostro():
    capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            alumno.rostro = face.tobytes()

            # Mostrar la imagen capturada en la interfaz gráfica
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image=image)
            label.config(image=photo)
            label.image = photo

            messagebox.showinfo("Éxito", "Rostro capturado para el alumno")

        # Salir del bucle después de capturar un rostro
        if alumno.rostro:
            break

    capture.release()

# Crear una ventana Tkinter
root = tk.Tk()
root.title("Sistema de Registro de Asistencia facial de Alumnos")

# Aplicar un estilo de ttkthemes
style = ThemedStyle(root)
style.set_theme("plastik")

# Crear una etiqueta para mostrar la imagen capturada
label = tk.Label(root)
label.pack()

# Crear un marco para ingresar los datos del alumno
frame = ttk.LabelFrame(root, text="Datos del Alumno")
frame.pack(padx=10, pady=10)

nombre_label = ttk.Label(frame, text="Nombre del Alumno:")
nombre_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

nombre_entry = ttk.Entry(frame)
nombre_entry.grid(row=0, column=1, padx=5, pady=5)

apellido_label = ttk.Label(frame, text="Apellido del Alumno:")
apellido_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

apellido_entry = ttk.Entry(frame)
apellido_entry.grid(row=1, column=1, padx=5, pady=5)

codigo_label = ttk.Label(frame, text="Código del Alumno:")
codigo_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

codigo_entry = ttk.Entry(frame)
codigo_entry.grid(row=2, column=1, padx=5, pady=5)

# Botón para registrar al alumno
registrar_button = ttk.Button(frame, text="Registrar Alumno", command=registrar_alumno)
registrar_button.grid(row=3, columnspan=2, pady=10)

# Botón para capturar el rostro del alumno
capturar_button = ttk.Button(root, text="Capturar Rostro", command=capturar_rostro)
capturar_button.pack(pady=10)

# Crea un objeto Alumno
alumno = Alumno("", "","")

root.mainloop()
