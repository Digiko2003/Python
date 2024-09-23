import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import PyPDF2
#pip install PyPDF2


# Función para seleccionar los archivos PDF
def seleccionar_pdfs():
    archivos = filedialog.askopenfilenames(title="Selecciona archivos PDF", 
                                           filetypes=[("Archivos PDF", "*.pdf")])
    lista_pdfs.delete(0, tk.END)  # Limpiar lista antes de añadir
    for archivo in archivos:
        lista_pdfs.insert(tk.END, archivo)  # Añadir cada archivo seleccionado a la lista

# Función para mover un archivo hacia arriba en la lista
def mover_arriba():
    seleccion = lista_pdfs.curselection()
    if seleccion:
        idx = seleccion[0]
        if idx > 0:
            archivo = lista_pdfs.get(idx)
            lista_pdfs.delete(idx)
            lista_pdfs.insert(idx - 1, archivo)
            lista_pdfs.select_set(idx - 1)

# Función para mover un archivo hacia abajo en la lista
def mover_abajo():
    seleccion = lista_pdfs.curselection()
    if seleccion:
        idx = seleccion[0]
        if idx < lista_pdfs.size() - 1:
            archivo = lista_pdfs.get(idx)
            lista_pdfs.delete(idx)
            lista_pdfs.insert(idx + 1, archivo)
            lista_pdfs.select_set(idx + 1)

# Función para unir los archivos PDF
def unir_pdfs():
    lista_archivos = lista_pdfs.get(0, tk.END)
    if len(lista_archivos) < 2:
        messagebox.showwarning("Advertencia", "Debes seleccionar al menos dos archivos PDF.")
        return

    archivo_salida = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                  filetypes=[("Archivos PDF", "*.pdf")],
                                                  title="Guardar archivo combinado como")
    
    if archivo_salida:
        fusionador = PyPDF2.PdfMerger()
        for pdf in lista_archivos:
            with open(pdf, 'rb') as archivo:
                fusionador.append(archivo)
        
        with open(archivo_salida, 'wb') as salida:
            fusionador.write(salida)
        
        messagebox.showinfo("Éxito", f"Archivos combinados en {archivo_salida}")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Unir PDFs")

# Botón para seleccionar archivos
btn_seleccionar = tk.Button(ventana, text="Seleccionar PDFs", command=seleccionar_pdfs)
btn_seleccionar.pack(pady=10)

# Lista para mostrar los archivos seleccionados
lista_pdfs = Listbox(ventana, selectmode=tk.SINGLE, width=60, height=10)
lista_pdfs.pack(padx=10, pady=10)

# Botones para ordenar los archivos
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

btn_arriba = tk.Button(frame_botones, text="Mover Arriba", command=mover_arriba)
btn_arriba.grid(row=0, column=0, padx=5)

btn_abajo = tk.Button(frame_botones, text="Mover Abajo", command=mover_abajo)
btn_abajo.grid(row=0, column=1, padx=5)

# Botón para unir PDFs
btn_unir = tk.Button(ventana, text="Unir PDFs", command=unir_pdfs)
btn_unir.pack(pady=20)

# Iniciar la ventana principal
ventana.mainloop()
