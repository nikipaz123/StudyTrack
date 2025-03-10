import os
import tkinter as tk
from tkinter import ttk, messagebox
import pygame
from PIL import Image, ImageTk

def audio():
    pygame.mixer.init()

    base_path = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_path, "audios")

    # Lista de archivos de audio
    audio_files = {
        "Librería": os.path.join(audio_folder, "libreria.mp3"),
        "Lluvia": os.path.join(audio_folder, "lluvia.mp3"),
        "Ruido Blanco": os.path.join(audio_folder, "white_noise.mp3"),
        "Cafetería + Jazz": os.path.join(audio_folder, "cafeteria.mp3"),
        "Lo-Fi Beats": os.path.join(audio_folder, "lofi.mp3"),
        "Musica de Minecraft": os.path.join(audio_folder, "minecraftmusic.mp3"),
        "Keyboard Typying": os.path.join(audio_folder, "typing.mp3"),
        "Musica Clasica": os.path.join(audio_folder, "clasico.mp3"),
    }

    # Verifica si los archivos de audio existen
    for key, path in audio_files.items():
        if not os.path.isfile(path):
            print(f"Advertencia: No se encontró el archivo de audio para '{key}' en: {path}")

    def play_sound():
        selected_sound = sound_var.get()
        if selected_sound and selected_sound in audio_files:
            try:
                file_path = audio_files[selected_sound]
                if os.path.isfile(file_path):
                    pygame.mixer.music.load(file_path)
                    pygame.mixer.music.play(-1)  # Reproduce en bucle
                else:
                    print(f"Archivo de audio no encontrado: {file_path}")
                    messagebox.showerror("Error", f"Archivo de audio no encontrado: {selected_sound}")
            except Exception as e:
                print(f"Error al reproducir el audio: {e}")
                messagebox.showerror("Error", f"Error al reproducir el audio: {e}")

    def pause_sound():
        pygame.mixer.music.pause()

    def resume_sound():
        pygame.mixer.music.unpause()

    def on_close(): #el error que esta el documento
        pygame.mixer.music.stop()
        root.destroy()

    ruta_imagen = os.path.join(base_path, 'vinilo.gif')

    # Verifica si el GIF existe
    if not os.path.isfile(ruta_imagen):
        print(f"Advertencia: El archivo 'vinilo.gif' no existe en: {ruta_imagen}")
        messagebox.showerror("Error", "El archivo 'vinilo.gif' no se encontró.")
        return

    gif_frames = []

    root = tk.Toplevel()
    root.title("Reproductor de Sonidos de Estudio")
    root.geometry("400x300")
    font_large = ("Arial", 14)

    try:
        gif = Image.open(ruta_imagen)
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = ImageTk.PhotoImage(gif.resize((400, 300)).convert("RGB"))
            gif_frames.append(frame_image)

        label_fondo = tk.Label(root, image=gif_frames[0])
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        def animar_gif(indice):
            nuevo_frame = gif_frames[indice]
            label_fondo.config(image=nuevo_frame)
            root.after(100, animar_gif, (indice + 1) % len(gif_frames))

        animar_gif(0)
    except Exception as e:
        print(f"Error al cargar o animar el GIF: {e}")
        messagebox.showerror("Error", f"Error al cargar o animar el GIF: {e}")

    sound_var = tk.StringVar()
    sound_var.set("Elija Una Opción")

    sound_menu = ttk.Combobox(
        root,
        textvariable=sound_var,
        values=list(audio_files.keys()),
        state="readonly",
        font=font_large,
        width=25,
    )
    sound_menu.pack(pady=10)

    play_button = tk.Button(
        root, text="▶️ Reproducir", command=play_sound,
        font=font_large, width=15, bg="gray", fg="white", relief="flat"
    )
    play_button.pack(pady=5)

    pause_button = tk.Button(
        root, text="⏸️ Pausar", command=pause_sound,
        font=font_large, width=15, bg="gray", fg="white"
    )
    pause_button.pack(pady=5)

    resume_button = tk.Button(
        root, text="⏯️ Reanudar", command=resume_sound,
        font=font_large, width=15, bg="gray", fg="white"
    )
    resume_button.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

