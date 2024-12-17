import customtkinter as ctk
from tkinter import filedialog
from moviepy import VideoFileClip

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Conversor MP4 a MP3")
        self.geometry("400x200")

        self.label = ctk.CTkLabel(self, text="Selecciona un archivo .mp4")
        self.label.pack(pady=20)

        self.select_button = ctk.CTkButton(self, text="Seleccionar archivo", command=self.select_file)
        self.select_button.pack(pady=10)

        self.convert_button = ctk.CTkButton(self, text="Convertir a .mp3", command=self.convert_to_mp3)
        self.convert_button.pack(pady=10)

        self.file_path = ""

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Archivos MP4", "*.mp4")])
        if self.file_path:
            self.label.configure(text=f"Archivo seleccionado: {self.file_path}")

    def convert_to_mp3(self):
        if self.file_path:
            mp3_file = self.file_path.rsplit('.', 1)[0] + '.mp3'
            video = VideoFileClip(self.file_path)
            video.audio.write_audiofile(mp3_file)
            video.close()
            self.label.configure(text=f"Convertido a: {mp3_file}")
        else:
            self.label.configure(text="Por favor, selecciona un archivo .mp4 primero.")

if __name__ == "__main__":
    app = App()
    app.mainloop()