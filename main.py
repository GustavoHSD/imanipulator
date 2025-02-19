from tkinter import Button, Frame, Label, Tk, filedialog, messagebox, ttk
from tkinter.font import Font
import numpy as np
import os
import rembg
from pathlib import Path
from PIL import ImageTk, Image

DOWNLOADS_DIR = os.path.join(Path.home() / "Downloads")

class PreviewImageWidget(Frame):
    def __init__(self, parent=None):
        super().__init__(parent, padx=1, pady=1, height=110, background='grey')
        self.config(width=400)
        self.images_path = []
        self.images_thumb = []
        self.label = Label(self, text="Nenhuma imagem carregada", padx=5, pady=5, background='white', height=4)
        self.label.grid(column=0, row=1, sticky='ew')

    def reload(self):
        if self.images_path:
            self.label.grid_forget()
        else:
            self.label.grid(sticky='ew')

        for i, image_path in enumerate(self.images_path):
            try:
                image = Image.open(image_path)
                image.thumbnail((80, 80))
                image_tk = ImageTk.PhotoImage(image)
                self.images_thumb.append(image_tk)
                label = Label(self, image=image_tk)
                label.grid(column=i, row=1, sticky='ew')

            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

class Actions(Frame):
    def __init__(self, parent=None, images_path: list[str] = []):
        super().__init__(parent, padx=1, pady=1)
        self.output_dir = ""
        self.images_path = images_path 
        self.canvas_size = (800, 800)

        rembgButton = Button(self, text="Remover fundo", command=self.remove_background)
        rembgButton.grid(column=0, row=0)
        resizeButton = Button(self, text="Redimencionar", command=self.resize)
        resizeButton.grid(column=1, row=0)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=100)
        self.progress_bar_label = Label(self, text="Aguardando acao...")
        self.progress_bar_separator = ttk.Separator(self, orient="horizontal")

        self.status_label = Label(self, text="")
        self.status_separator = ttk.Separator(self, orient="horizontal")

    def load_progress(self):
        self.progress_bar_separator.grid(column=0, row=3, pady=(10, 1), sticky='ew', columnspan=2)
        self.progress_bar_label.grid(column=0, row=4, columnspan=2, pady=0)
        self.progress_bar.grid(column=0, row=5, columnspan=2)
    
    def destroy_progress_bar(self):
        self.progress_bar_separator.grid_forget()
        self.progress_bar_label.grid_forget()
        self.progress_bar.grid_forget()

    def load_status(self, status):
        self.status_separator.grid(column=0, row=3, pady=(10, 1), sticky='ew', columnspan=2)
        self.status_separator.grid(column=0, row=4, columnspan=2, pady=0)
        self.status_label["text"] = status
        self.status_label.grid(column=0, row=4, columnspan=2, pady=0)

    def check(self):
        if not self.images_path:
            messagebox.showerror("Erro!", "Nenhuma Imagem selecionada")
            return
        if self.output_dir == "":
            self.output_dir = filedialog.askdirectory(title="Selecione a pasta de salvamento", initialdir=DOWNLOADS_DIR)

    def remove_background(self):
        self.check() 
        os.makedirs(self.output_dir, exist_ok=True)
        try:
            self.progress_bar["value"] = 0 
            self.progress_bar["maximum"] = len(self.images_path)
            self.progress_bar_label["text"] = "Removendo fundo..."
            for i, file_path in enumerate(self.images_path):
                input_image = Image.open(file_path).convert("RGB")
                input_array = np.array(input_image) 
                input_image.thumbnail(self.canvas_size)
                white_bg = Image.new("RGB", self.canvas_size, (255, 255, 255))
                position = ((self.canvas_size[0] - input_image.width) // 2,
                            (self.canvas_size[1] - input_image.height) // 2)
                white_bg.paste(input_image, position)
                output_array = rembg.remove(input_array)
                output_image = Image.fromarray(output_array)
                input_image = Image.open(file_path).convert("RGB") 
                input_image.thumbnail(self.canvas_size)
                white_bg.paste(input_image, position)
                output_name = f'{i}_no-bg.jpg' 
                output_image.save(os.path.join(self.output_dir, output_name), "PNG")  
                self.progress_bar["value"] = i + 1
                self.update_idletasks()

            self.destroy_progress_bar()
            messagebox.showinfo("Sucesso!", "Imagens salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro!", f"Um erro aconteceu: {e}")

    def resize(self):
        self.check()
        os.makedirs(self.output_dir, exist_ok=True)
        try:
            for i, file_path in enumerate(self.images_path):
                input_image = Image.open(file_path).convert("RGB")
                input_image.thumbnail(self.canvas_size)
                white_bg = Image.new("RGB", self.canvas_size, (255, 255, 255))
                position = ((self.canvas_size[0] - input_image.width) // 2,
                            (self.canvas_size[1] - input_image.height) // 2) 
                white_bg.paste(input_image, position)
                output_name = f'{i}-resized.jpg'
                white_bg.save(os.path.join(self.output_dir, output_name), "JPEG")
            
            messagebox.showinfo("Sucesso!", "Imagens salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro!", f"Um erro aconteceu: {e}")

def select_image(imgWidget: PreviewImageWidget, actions: Actions):
    imgWidget.images_path = list(filedialog.askopenfilenames(
            title="Selecione uma imagem",
            initialdir=DOWNLOADS_DIR,
            filetypes=(("Images", ["*.jpg", "*.jpeg", "*.png", "*.webp"]), ),
        ))
    actions.images_path = imgWidget.images_path
    actions.load_progress()
    imgWidget.reload()

if __name__ == "__main__":
    root = Tk()
    root.title("Imanipulator")

    mainframe = Frame(root, width=100, padx=5, pady=5)
    mainframe.grid(column=0, row=0, columnspan=1)

    titleFont = Font(family='Noto Sans Mono CJK JP', weight='bold', size=24)
    title = Label(mainframe, text="Imanipulator", font=titleFont)
    title.grid(column=0, row=1, columnspan=1)

    seletectImgPreview = PreviewImageWidget(mainframe)
    seletectImgPreview.grid(column=0, row=3)

    actions = Actions(mainframe)
    actions.grid(column=0, row=5)

    selectImageButton = Button(mainframe, text="Carregar imagens", command=lambda: select_image(seletectImgPreview, actions))
    selectImageButton.grid(column=0, row=4, pady=5)

    root.mainloop()
