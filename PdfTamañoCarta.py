import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

# Dimensiones de tamaño carta en puntos PDF (8.5 x 11 pulgadas)
TAMANO_CARTA = (612, 792)  # (ancho, alto)

# Función para redimensionar el PDF a tamaño carta
def redimensionar_pdf_a_tamano_carta(pdf_entrada, pdf_salida):
    try:
        # Abrir el archivo PDF de entrada
        with open(pdf_entrada, 'rb') as archivo_pdf:
            lector_pdf = PyPDF2.PdfReader(archivo_pdf)
            escritor_pdf = PyPDF2.PdfWriter()

            # Redimensionar cada página al tamaño carta
            for pagina in lector_pdf.pages:
                # Obtener las dimensiones originales de la página
                pagina_media_box = pagina.mediabox
                ancho_original = pagina_media_box.width
                alto_original = pagina_media_box.height

                # Calcular los factores de escala
                escala_x = TAMANO_CARTA[0] / ancho_original
                escala_y = TAMANO_CARTA[1] / alto_original

                # Escalar la página manteniendo su contenido
                pagina.scale(escala_x, escala_y)

                # Añadir la página redimensionada al escritor de PDF
                escritor_pdf.add_page(pagina)

            # Escribir el archivo PDF de salida
            with open(pdf_salida, 'wb') as archivo_pdf_salida:
                escritor_pdf.write(archivo_pdf_salida)

        messagebox.showinfo("Éxito", f"El archivo PDF ha sido redimensionado a tamaño carta y guardado como {pdf_salida}.")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo redimensionar el PDF. Error: {e}")

# Función para abrir una ventana de selección de archivo y redimensionar el PDF
def seleccionar_pdf():
    # Abrir ventana de diálogo para seleccionar el archivo PDF de entrada
    archivo_entrada = filedialog.askopenfilename(title="Seleccionar PDF", 
                                                 filetypes=[("Archivos PDF", "*.pdf")])
    if archivo_entrada:
        # Abrir ventana de diálogo para seleccionar dónde guardar el archivo de salida
        archivo_salida = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                      filetypes=[("Archivos PDF", "*.pdf")],
                                                      title="Guardar archivo redimensionado como")
        if archivo_salida:
            redimensionar_pdf_a_tamano_carta(archivo_entrada, archivo_salida)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Redimensionar PDF a Tamaño Carta")

# Botón para seleccionar el archivo PDF y redimensionarlo
btn_seleccionar = tk.Button(ventana, text="Seleccionar y Redimensionar PDF", command=seleccionar_pdf)
btn_seleccionar.pack(pady=20)

# Iniciar la ventana principal
ventana.mainloop()
