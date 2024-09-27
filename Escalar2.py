import os
from PIL import Image
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

# Funciónes
def resize_images(input_folder, output_zip, scale=0.5):
    temp_files = []

    # Asegúrate de que la carpeta de salida exista
    output_dir = os.path.dirname(output_zip)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                img_path = os.path.join(root, file)
                try:
                    with Image.open(img_path) as img:
                        original_width, original_height = img.size
                        new_width = int(original_width * scale)
                        new_height = int(original_height * scale)

                        # Redimensionar la imagen
                        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                        # Guardar la imagen temporalmente
                        temp_file_path = os.path.join(root, f"resized_{file}")
                        resized_img.save(temp_file_path)
                        temp_files.append(temp_file_path)
                except Exception as e:
                    print(f"Error procesando {file}: {e}")

    # Crear el archivo ZIP y añadir las imágenes redimensionadas
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for temp_file in temp_files:
            zipf.write(temp_file, os.path.basename(temp_file))

    # Eliminar las imágenes temporales
    for temp_file in temp_files:
        os.remove(temp_file)

    messagebox.showinfo("Éxito", f"Las imágenes han sido redimensionadas y comprimidas en {output_zip}.")

# Función para abrir la ventana de selección de carpeta
def seleccionar_carpeta():
    carpeta_entrada = filedialog.askdirectory(title="Seleccionar carpeta con imágenes")
    if carpeta_entrada:
        seleccionar_salida(carpeta_entrada)

# Función para seleccionar la ubicación del archivo ZIP de salida
def seleccionar_salida(carpeta_entrada):
    archivo_salida = filedialog.asksaveasfilename(defaultextension=".zip", 
                                                  filetypes=[("Archivo ZIP", "*.zip")],
                                                  title="Guardar archivo ZIP")
    if archivo_salida:
        resize_images(carpeta_entrada, archivo_salida)

# Crear ventana principal con tkinter
ventana = tk.Tk()
ventana.title("Redimensionar y Comprimir Imágenes")

# Botón para seleccionar carpeta y archivo de salida
btn_seleccionar = tk.Button(ventana, text="Seleccionar carpeta y redimensionar imágenes", command=seleccionar_carpeta)
btn_seleccionar.pack(pady=20)

# Ejecutar la ventana
ventana.mainloop()
