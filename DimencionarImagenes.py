import os
from PIL import Image
import zipfile
#pip install pillow

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

                        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                        temp_file_path = os.path.join(root, f"resized_{file}")
                        resized_img.save(temp_file_path)
                        temp_files.append(temp_file_path)
                except Exception as e:
                    print(f"Error procesando {file}: {e}")

    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for temp_file in temp_files:
            zipf.write(temp_file, os.path.basename(temp_file))

    for temp_file in temp_files:
        os.remove(temp_file)

    print(f"Las imágenes han sido redimensionadas y comprimidas en {output_zip}.")

if __name__ == "__main__":
    input_folder = input("Introduce la ruta de la carpeta con las imágenes: ")
    output_zip = r"C:\Users\digik\Downloads\doujin2.zip"  # Cambia esta ruta según tus necesidades
    resize_images(input_folder, output_zip)
