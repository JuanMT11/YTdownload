import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pytube import YouTube
from moviepy.editor import AudioFileClip

class DescargadorYouTube:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de YouTube")

        self.parent_dir = os.getcwd()

        self.enlace_var = tk.StringVar()
        self.opcion_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Enlace de YouTube:").grid(row=0, column=0, pady=10)
        ttk.Entry(self.root, textvariable=self.enlace_var, width=40).grid(row=0, column=1, pady=10)

        ttk.Radiobutton(self.root, text="Descargar video (mp4)", variable=self.opcion_var, value="video").grid(row=1, column=0, columnspan=2, pady=5)
        ttk.Radiobutton(self.root, text="Descargar música (mp3)", variable=self.opcion_var, value="audio").grid(row=2, column=0, columnspan=2, pady=5)

        ttk.Button(self.root, text="Descargar", command=self.iniciar_descarga).grid(row=3, column=0, columnspan=2, pady=10)

    def iniciar_descarga(self):
        enlace = self.enlace_var.get()
        opcion = self.opcion_var.get()

        if not enlace:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un enlace de YouTube.")
            return

        self.inicia_proceso_descarga(enlace, opcion)
        messagebox.showinfo("Descarga completada", "Descarga completada")

    def inicia_proceso_descarga(self, link, opcion):
        try:
            yt = YouTube(link)
        except:
            messagebox.showerror("Error", f"Error en el enlace: {link}")
            return

        if opcion == 'video':
            stream = yt.streams.filter(progressive=True).first()
            stream.download(os.path.join(self.parent_dir, 'descargas'))
        elif opcion == 'audio':
            audio_stream = yt.streams.get_audio_only()
            audio_path = audio_stream.download(os.path.join(self.parent_dir, 'descargas'))
            self.convertir_a_mp3(audio_path)

    def convertir_a_mp3(self, audio_path):
        audioclip = AudioFileClip(audio_path)
        mp3_path = audio_path.replace('.mp4', '.mp3')
        audioclip.write_audiofile(mp3_path)
        os.remove(audio_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = DescargadorYouTube(root)
    root.mainloop()

