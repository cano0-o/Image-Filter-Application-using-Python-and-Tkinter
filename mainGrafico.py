# Importación de librerías necesarias
import tkinter as tk
from tkinter import filedialog  # Para abrir y guardar archivos
from PIL import Image, ImageTk  # Para manipulación y visualización de imágenes
import numpy as np  # Para operaciones matriciales y manipulación de imágenes
import random  # Para generar ruido aleatorio


# ============================
# FUNCIÓN PARA ABRIR ARCHIVO
# ============================
def abrir_archivo():
    """Abre un cuadro de diálogo para seleccionar una imagen (JPG o PNG) y cargarla."""
    ruta_archivo = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.png")]
    )
    if ruta_archivo:
        cargar_imagen(ruta_archivo)


# ============================
# FUNCIÓN PARA CARGAR IMAGEN
# ============================
def cargar_imagen(ruta):
    """Carga la imagen seleccionada, la ajusta al tamaño de la ventana y la muestra."""
    global imagen_original, imagen_rotada
    imagen_original = Image.open(ruta)  # Abre la imagen
    imagen_rotada = None  # Reinicia la imagen rotada si hay una imagen nueva
    imagen = imagen_original.resize((400, 400), Image.LANCZOS)  # Redimensiona la imagen
    img = ImageTk.PhotoImage(imagen)
    label_imagen.config(image=img)
    label_imagen.image = img


# ============================
# FUNCIÓN PARA APLICAR BLANCO Y NEGRO
# ============================
def aplicar_bn():
    """Convierte la imagen original a escala de grises aplicando ponderación de canales RGB."""
    if imagen_original:
        canal_R, canal_G, canal_B = extraer_canales(imagen_original)
        imagen_grises = 0.299 * canal_R + 0.587 * canal_G + 0.114 * canal_B
        imagen_grises = np.clip(imagen_grises, 0, 255).astype(np.uint8)

        # Convierte la matriz resultante a imagen
        imagen_bn = Image.fromarray(imagen_grises)
        img_bn = ImageTk.PhotoImage(imagen_bn.resize((400, 400), Image.LANCZOS))
        label_imagen.config(image=img_bn)
        label_imagen.image = img_bn


# ============================
# FUNCIÓN PARA EXTRAER CANALES RGB
# ============================
def extraer_canales(imagen):
    """Extrae los canales RGB de la imagen y los devuelve como matrices."""
    matriz = np.array(imagen)
    canal_R = matriz[:, :, 0]  # Canal rojo
    canal_G = matriz[:, :, 1]  # Canal verde
    canal_B = matriz[:, :, 2]  # Canal azul
    return canal_R, canal_G, canal_B


# ============================
# FUNCIÓN PARA APLICAR RUIDO
# ============================
def aplicar_ruido():
    """Agrega ruido aleatorio a la imagen original y la muestra."""
    if imagen_original:
        ruido_imagen = agregar_ruido(imagen_original)
        img_ruido = ImageTk.PhotoImage(ruido_imagen.resize((400, 400), Image.LANCZOS))
        label_imagen.config(image=img_ruido)
        label_imagen.image = img_ruido


# ============================
# FUNCIÓN PARA AGREGAR RUIDO ALEATORIO
# ============================
def agregar_ruido(imagen, porcentaje_ruido=0.10):
    """Introduce ruido aleatorio en la imagen, con un porcentaje especificado."""
    arreglo_imagen = np.array(imagen)
    filas, columnas, canales = arreglo_imagen.shape
    total_pixeles = filas * columnas
    num_pixeles_ruido = int(porcentaje_ruido * total_pixeles)

    # Añadir píxeles blancos
    for _ in range(num_pixeles_ruido // 2):
        y = random.randint(0, filas - 1)
        x = random.randint(0, columnas - 1)
        arreglo_imagen[y][x] = [255, 255, 255]  # Píxel blanco

    # Añadir píxeles negros
    for _ in range(num_pixeles_ruido // 2):
        y = random.randint(0, filas - 1)
        x = random.randint(0, columnas - 1)
        arreglo_imagen[y][x] = [0, 0, 0]  # Píxel negro

    return Image.fromarray(arreglo_imagen)


# ============================
# FUNCIÓN PARA GUARDAR IMAGEN
# ============================
def guardar_imagen():
    """Guarda la imagen procesada en formato PNG o JPEG."""
    if imagen_original:
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
        )
        if ruta_guardado:
            imagen_original.save(ruta_guardado)


# ============================
# FUNCIÓN PARA SUPERPONER STICKER
# ============================
def superponer_imagen():
    """Superpone una imagen (sticker) en la esquina inferior derecha de la imagen original."""
    if imagen_original:
        img2 = Image.open("/Users/can0o/Documentos/Graficación/gatito.png").convert(
            "RGBA"
        )
        img2 = img2.resize((100, 100))  # Redimensiona el sticker

        img1 = imagen_original.convert("RGB")
        img1_width, img1_height = img1.size

        position = (
            img1_width - img2.width - 10,
            img1_height - img2.height - 10,
        )  # Posición en la esquina inferior derecha
        pixels1 = img1.load()
        pixels2 = img2.load()

        # Mezcla píxeles del sticker y la imagen original
        for i in range(img2.width):
            for j in range(img2.height):
                img1_x = position[0] + i
                img1_y = position[1] + j
                r2, g2, b2, a2 = pixels2[i, j]

                if a2 == 0:
                    r1, g1, b1 = pixels1[img1_x, img1_y]
                    r = r1 ^ r2
                    g = g1 ^ g2
                    b = b1 ^ b2
                    pixels1[img1_x, img1_y] = (r, g, b)
                else:
                    pixels1[img1_x, img1_y] = (r2, g2, b2)

        img_superpuesta = ImageTk.PhotoImage(img1.resize((400, 400), Image.LANCZOS))
        label_imagen.config(image=img_superpuesta)
        label_imagen.image = img_superpuesta


# ============================
# FUNCIÓN PARA ROTAR IMAGEN 90°
# ============================
def rotar_90(imagen):
    """Rota la imagen 90 grados en sentido horario."""
    matriz_imagen = np.array(imagen)
    matriz_rotada = np.transpose(matriz_imagen, (1, 0, 2))  # Transpone la imagen
    matriz_rotada = np.flip(matriz_rotada, axis=1)  # Invierte horizontalmente
    imagen_rotada = Image.fromarray(matriz_rotada)
    return imagen_rotada


# ============================
# FUNCIÓN PARA APLICAR ROTACIÓN
# ============================
def aplicar_rotacion():
    """Aplica una rotación de 90° a la imagen y actualiza la vista."""
    global imagen_rotada
    if imagen_rotada:
        imagen_rotada = rotar_90(imagen_rotada)
    else:
        imagen_rotada = rotar_90(imagen_original)

    img_rotada = ImageTk.PhotoImage(imagen_rotada.resize((400, 400), Image.LANCZOS))
    label_imagen.config(image=img_rotada)
    label_imagen.image = img_rotada


# ============================
# FUNCIÓN PARA APLICAR ESPEJO
# ============================
def aplicar_espejo():
    """Aplica un efecto espejo horizontal a la imagen."""
    if imagen_original:
        imagen_espejo = np.flip(
            np.array(imagen_original), axis=1
        )  # Invierte horizontalmente
        imagen_espejo = Image.fromarray(imagen_espejo)
        img_espejo = ImageTk.PhotoImage(imagen_espejo.resize((400, 400), Image.LANCZOS))
        label_imagen.config(image=img_espejo)
        label_imagen.image = img_espejo


# ============================
# FUNCIÓN PARA RESTABLECER IMAGEN ORIGINAL
# ============================
def limpiar_filtros():
    """Restaura la imagen original después de aplicar filtros."""
    global imagen_rotada
    if imagen_original:
        imagen_rotada = None
        imagen = imagen_original.resize((400, 400), Image.LANCZOS)
        img = ImageTk.PhotoImage(imagen)
        label_imagen.config(image=img)
        label_imagen.image = img


# ============================
# CONFIGURACIÓN DE INTERFAZ
# ============================
ventana = tk.Tk()
ventana.title("Filtros App")  # Título de la ventana
ventana.geometry("800x700")  # Tamaño de la ventana
ventana.configure(bg="#f0f0f0")  # Color de fondo

# Estilo de los botones
fuente_boton = ("Helvetica", 12, "bold")


def estilo_boton(boton):
    """Aplica estilo uniforme a los botones."""
    boton.config(
        font=fuente_boton,
        bg="#4CAF50",  # Color de fondo
        fg="black",
        relief="flat",
        padx=10,
        pady=10,
        activebackground="#45a049",
        activeforeground="white",
        bd=0,
        highlightthickness=0,
    )


# ============================
# CREACIÓN DE BOTONES
# ============================
btn_archivo = tk.Button(ventana, text="Archivo", command=abrir_archivo)
btn_archivo.place(x=20, y=20, width=150, height=50)
estilo_boton(btn_archivo)

btn_bn = tk.Button(ventana, text="B/N", command=aplicar_bn)
btn_bn.place(x=20, y=80, width=150, height=50)
estilo_boton(btn_bn)

btn_ruido = tk.Button(ventana, text="Ruido", command=aplicar_ruido)
btn_ruido.place(x=20, y=140, width=150, height=50)
estilo_boton(btn_ruido)

btn_superponer = tk.Button(ventana, text="Sticker", command=superponer_imagen)
btn_superponer.place(x=20, y=200, width=150, height=50)
estilo_boton(btn_superponer)

btn_rotacion = tk.Button(ventana, text="Rotar 90°", command=aplicar_rotacion)
btn_rotacion.place(x=20, y=260, width=150, height=50)
estilo_boton(btn_rotacion)

btn_espejo = tk.Button(ventana, text="Espejo", command=aplicar_espejo)
btn_espejo.place(x=20, y=320, width=150, height=50)
estilo_boton(btn_espejo)

btn_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_filtros)
btn_limpiar.place(x=20, y=380, width=150, height=50)
estilo_boton(btn_limpiar)

btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_imagen)
btn_guardar.place(x=20, y=440, width=150, height=50)
estilo_boton(btn_guardar)

# ============================
# LABEL PARA MOSTRAR IMÁGENES
# ============================
label_imagen = tk.Label(ventana, bg="#f0f0f0")
label_imagen.place(x=200, y=20)

# Variables globales para almacenar imágenes
imagen_original = None
imagen_rotada = None

# Inicia la interfaz gráfica
ventana.mainloop()
