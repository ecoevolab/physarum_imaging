import cv2
import os
import re

def crear_video(carpeta_imagenes, salida='video.mp4', fps=24):

    archivos = [f for f in os.listdir(carpeta_imagenes) 
                if re.match(r'foto_\d+\.jpg', f, re.IGNORECASE)]
    
    # extraer el número del nombre
    archivos.sort(key=lambda x: int(re.search(r'foto_(\d+)\.jpg', x, re.IGNORECASE).group(1)))

    print(f"Encontradas {len(archivos)} imágenes:")

    # Leer primera imagen para obtener dimensiones
    primera_img = cv2.imread(os.path.join(carpeta_imagenes, archivos[0]))
        
    altura, ancho, _ = primera_img.shape
    print(f"Dimensiones del video: {ancho}x{altura}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(salida, fourcc, fps, (ancho, altura))

    for i, archivo in enumerate(archivos):
        ruta_completa = os.path.join(carpeta_imagenes, archivo)
        img = cv2.imread(ruta_completa)
        
        if img is None:
            print(f"Error al leer {archivo}")
            continue
            
        video.write(img)
        
        # Mostrar progreso cada 10 imágenes
        if (i + 1) % 10 == 0 or (i + 1) == len(archivos):
            print(f'Procesadas {i + 1}/{len(archivos)} imágenes')

    video.release()
    print(f'Video guardado')


# Versión con interfaz más amigable
def crear_video_interactivo():
    print("=== CREAR DE VIDEO DE PHYSARUM ===")
    
    # Solicitar ruta de la carpeta
    carpeta = input("Ruta de la carpeta con las imágenes: ").strip()
    
    if not os.path.exists(carpeta):
        print("carpeta no existe")
        return
    
    # Solicitar nombre del video de salida
    salida = input("Nombre del video [video.mp4]: ").strip()
    if not salida:
        salida = "video.mp4"
    elif not salida.endswith('.mp4'):
        salida += '.mp4'
    
    # Solicitar FPS
    try:
        fps = int(input("Cuadros por segundo (FPS) [24]: ").strip() or "24")
    except ValueError:
        fps = 24
        print("Usando valor por defecto: 24 FPS")
    
    crear_video(carpeta, salida, fps)

if __name__ == "__main__":

    opcion = input("¿Usar modo interactivo? (s/n) [s]: ").strip().lower()
    
    if opcion in ['s', 'si', 'sí', '']:
        crear_video_interactivo()
    else:
        # Configuración automática
        carpeta = "."  
        nombre_video = "Physarum.mp4"
        fps = 24
        
        crear_video(carpeta, nombre_video, fps)
