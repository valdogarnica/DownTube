import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import StringVar
from tkinter.ttk import Progressbar
import threading
import yt_dlp as youtube_dl
from PIL import Image
import os
from moviepy import VideoFileClip

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ruta base
IMAGES_DIR = os.path.join(BASE_DIR, "images")


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.iconbitmap(os.path.join(IMAGES_DIR, "dowYoutube.ico"))
        self.root.title("DESCARGA VIDEOS DE YOUTUBE")
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Imágenes
        down_icon = self.load_image("descargar.png", (30, 30))
        folder_icon = self.load_image("foldere.png", (30, 30))
        app_logo = self.load_image("dowYoutube.png", (100, 100))

        # Título e imagen principal
        ctk.CTkLabel(self.root, text="DESCARGA VIDEOS DEL YUTU", font=("Arial", 20, "bold"), text_color="red").pack(pady=10)
        ctk.CTkLabel(self.root, image=app_logo, text="").pack(pady=5)

        # Marco principal
        self.card = ctk.CTkFrame(master=self.root, corner_radius=15, width=350, height=400)
        self.card.pack(pady=10)

        # Campo URL
        self.url = ctk.CTkEntry(self.card, placeholder_text="Ingresa un Link de YouTube", width=500)
        self.url.pack(pady=10)

        # Botón de descarga
        self.download_button = ctk.CTkButton(self.card, text="Descargar", image=down_icon, width=400, height=50, fg_color="green", hover_color="black", command=self.start_download)
        self.download_button.pack(pady=10)

        # Selección de ruta
        ctk.CTkButton(self.card, text="Elegir Ruta", image=folder_icon, width=100, fg_color="blue", command=self.select_folder).pack(pady=10)
        self.save_path = StringVar()
        ctk.CTkLabel(self.card, textvariable=self.save_path).pack(pady=5)

        # Opciones de calidad
        self.quality = StringVar(value="best")
        ctk.CTkLabel(self.root, text="Selecciona calidad del video:").pack(pady=10)
        ctk.CTkComboBox(self.root, variable=self.quality, values=["best", "worst", "1080p", "720p"]).pack(pady=10)

        # Tipo de contenido
        self.download_type = StringVar(value="Video")
        ctk.CTkComboBox(self.root, variable=self.download_type, values=["Video", "Canción", "Ambos"]).pack(pady=10)

        # Barra de progreso
        ctk.CTkLabel(self.root, text="Progreso").pack(pady=10)
        self.progress_bar = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Texto de progreso
        self.progress_text = StringVar()
        self.progress_percentage = StringVar()
        ctk.CTkLabel(self.root, textvariable=self.progress_percentage).pack()
        ctk.CTkLabel(self.root, textvariable=self.progress_text).pack()

        # Firma
        ctk.CTkLabel(self.root, text="by: valentin GG", font=("Arial", 10, "bold"), text_color="blue").place(x=10, y=650)

    def load_image(self, filename, size):
        """Carga y redimensiona una imagen."""
        image = Image.open(os.path.join(IMAGES_DIR, filename))
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=image, size=size)

    def start_download(self):
        """Inicia la descarga en un hilo separado."""
        if not self.save_path.get():
            messagebox.showerror("Error", "Por favor, selecciona una ruta para guardar el archivo.")
            return

        if not self.url.get().strip():
            messagebox.showerror("Error", "Por favor, ingresa un enlace de YouTube.")
            return

        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
        """Descarga el video y actualiza el progreso."""
        url = self.url.get().strip()
        download_type = self.download_type.get()
        quality = self.quality.get()
        save_path = self.save_path.get()
        ydl_opts = {
            'format': quality,
            'outtmpl': os.path.join(self.save_path.get(), "%(title)s.%(ext)s"),
            'quiet': True,
            'progress_hooks': [self.update_progress],
        }

        try:
            # Descargar el video siempre
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                  #ydl.download([url])
                  info_dict = ydl.extract_info(url, download=True)
                  downloaded_file = ydl.prepare_filename(info_dict)
            
            self.file_path = downloaded_file
            if download_type == "Video":
                  messagebox.showinfo("Éxito", "¡Video descargado correctamente!")
            elif download_type == "Cancion":  # Cuando no sea "Video"
                  # Convertir el video descargado a MP3
                  mp3_file = self.file_path.rsplit('.', 1)[0] + '.mp3'
                  video = VideoFileClip(self.file_path)
                  video.audio.write_audiofile(mp3_file)
                  video.close()
                  # Eliminar el archivo de video .mp4
                  if os.path.exists(self.file_path):  # Verifica que el archivo existe
                        os.remove(self.file_path)  # Elimina el archivo
                        print(f"Archivo {self.file_path} eliminado correctamente.")
                  # Actualizar la interfaz gráfica
                  #self.label.configure(text=f"Convertido a: {mp3_file}")
                  messagebox.showinfo("Éxito", "¡Cancion Descargada con exito!")
            else:
                  mp3_file = self.file_path.rsplit('.', 1)[0] + '.mp3'
                  video = VideoFileClip(self.file_path)
                  video.audio.write_audiofile(mp3_file)
                  video.close()
                  
                  # Actualizar la interfaz gráfica
                  #self.label.configure(text=f"Convertido a: {mp3_file}")
                  messagebox.showinfo("Éxito", "¡Cancion Y Video Descargados con exito!")
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar o convertir: {str(e)}")

    def update_progress(self, d):
        """Actualiza la barra de progreso."""
        if d['status'] == 'downloading':
            total = d.get('total_bytes', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                progress = downloaded / total
                self.progress_bar['value'] = progress * 100
                self.progress_percentage.set(f"{int(progress * 100)}%")
                self.progress_text.set(f"{downloaded / 1e6:.2f} MB / {total / 1e6:.2f} MB")

    def select_folder(self):
        """Selecciona una carpeta de guardado."""
        folder = filedialog.askdirectory(title="Selecciona la carpeta para guardar")
        if folder:
            self.save_path.set(folder)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
