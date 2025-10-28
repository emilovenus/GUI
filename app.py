# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageSequence
import os, random, webbrowser
from manager import EmployeeManager

# --- Helpers para crear botones redondeados con Pillow ---
def create_rounded_button_image(text, width=180, height=45, radius=22, base_color=(70,130,180), text_color=(255,255,255), shadow=False, font_path=None, font_size=16):
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    rect_color = base_color
    # Sombra
    if shadow:
        shadow_img = Image.new("RGBA", (width, height), (0,0,0,0))
        sd = ImageDraw.Draw(shadow_img)
        sd.rounded_rectangle((4,4,width-4,height-4), radius=radius, fill=(0,0,0,120))
        img = Image.alpha_composite(shadow_img, img)
        draw = ImageDraw.Draw(img)
    # Botón
    draw.rounded_rectangle((0,0,width, height), radius=radius, fill=rect_color)
    # Texto
    if font_path and os.path.exists(font_path):
        try:
            f = ImageFont.truetype(font_path, font_size)
        except Exception:
            f = ImageFont.load_default()
    else:
        f = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=f)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text(((width-w)/2,(height-h)/2), text, font=f, fill=text_color)
    return img

# --- GUI principal ---
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.manager = EmployeeManager()
        self.master.geometry("900x600")
        self.grid(sticky="nsew")
        self.assets = {}
        self.load_assets()
        self.create_widgets()
        self.refresh_employees()

    def load_assets(self):
        # Cargar background si existe
        if os.path.exists("background.png"):
            img = Image.open("background.png").convert("RGBA")
            img = img.resize((900,600), Image.LANCZOS)
            self.assets["bg_img"] = ImageTk.PhotoImage(img)
        # Fuente pixel opcional
        self.assets["font_path"] = "pixel.ttf" if os.path.exists("pixel.ttf") else None
        # GIF saludo
        if os.path.exists("saludo.gif"):
            self.assets["saludo_gif"] = "saludo.gif"

    def create_widgets(self):
        # Fondo
        if "bg_img" in self.assets:
            self.canvas = tk.Canvas(self, width=900, height=600, highlightthickness=0)
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.canvas.create_image(0,0,anchor="nw", image=self.assets["bg_img"])
            container = tk.Frame(self.canvas, bg="#ffffff", bd=0)
            # colocar frame transparente con background semi-transparente
            self.canvas.create_window(450,300, window=container, width=820, height=520)
        else:
            container = tk.Frame(self, bg="#f0f0f0")
            container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Estilos y fuentes
        self.pixel_font = None
        if self.assets.get("font_path"):
            try:
                self.pixel_font = tkfont.Font(family="PixelFont", size=10)
            except Exception:
                self.pixel_font = None

        # Encabezado
        header = tk.Label(container, text="Registro de Empleados", font=("Segoe UI", 18, "bold"), bg="#ffffff")
        header.pack(pady=(10,8))

        # Formulario arriba
        form_frame = tk.Frame(container, bg="#ffffff")
        form_frame.pack(pady=6, padx=12, fill="x")

        tk.Label(form_frame, text="Nombre:", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.entry_nombre = ttk.Entry(form_frame, width=30)
        self.entry_nombre.grid(row=0, column=1, sticky="w", padx=5, pady=4)

        tk.Label(form_frame, text="Sexo:", bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.entry_sexo = ttk.Entry(form_frame, width=10)
        self.entry_sexo.grid(row=1, column=1, sticky="w", padx=5, pady=4)

        tk.Label(form_frame, text="Correo:", bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.entry_correo = ttk.Entry(form_frame, width=30)
        self.entry_correo.grid(row=2, column=1, sticky="w", padx=5, pady=4)

        # Botones principales (con imágenes)
        buttons_frame = tk.Frame(container, bg="#ffffff")
        buttons_frame.pack(pady=10)

        # Crear imágenes de botón (base)
        self.btn_imgs = {}
        # colores: añadir=verde, eliminar=rojo, refrescar=azul, export=moradito, mensaje=amarillo, cerrar=gris
        colors = {
            "add": (46,204,113),
            "delete": (231,76,60),
            "refresh": (52,152,219),
            "export": (155,89,182),
            "msg": (241,196,15),
            "close": (127,140,141)
        }
        for k,c in colors.items():
            img = create_rounded_button_image(
                text={"add":"Añadir","delete":"Eliminar","refresh":"Refrescar","export":"Hackear Ilegalmente la Base de Datos","msg":"Click aquí para mensaje interesante","close":"Cerrar"}[k],
                width=220 if k in ("export","msg") else 120,
                height=44,
                radius=22,
                base_color=c,
                text_color=(255,255,255),
                shadow=True,
                font_path=self.assets.get("font_path")
            )
            self.btn_imgs[k] = ImageTk.PhotoImage(img)

        # Buttons
        self.btn_add = tk.Button(buttons_frame, image=self.btn_imgs["add"], bd=0, command=self.add_employee, cursor="hand2")
        self.btn_add.grid(row=0, column=0, padx=6)
        self.add_hover_effect(self.btn_add, "add")

        self.btn_delete = tk.Button(buttons_frame, image=self.btn_imgs["delete"], bd=0, command=self.delete_selected, cursor="hand2")
        self.btn_delete.grid(row=0, column=1, padx=6)
        self.add_hover_effect(self.btn_delete, "delete")

        self.btn_refresh = tk.Button(buttons_frame, image=self.btn_imgs["refresh"], bd=0, command=self.refresh_employees, cursor="hand2")
        self.btn_refresh.grid(row=0, column=2, padx=6)
        self.add_hover_effect(self.btn_refresh, "refresh")

        # Export / mensaje / close on second row
        self.btn_export = tk.Button(buttons_frame, image=self.btn_imgs["export"], bd=0, command=self.export_csv, cursor="hand2")
        self.btn_export.grid(row=1, column=0, columnspan=2, pady=8)
        self.add_hover_effect(self.btn_export, "export")

        self.btn_msg = tk.Button(buttons_frame, image=self.btn_imgs["msg"], bd=0, command=self.open_message_window, cursor="hand2")
        self.btn_msg.grid(row=1, column=2, padx=8)
        self.add_hover_effect(self.btn_msg, "msg")

        # Tabla de empleados
        table_frame = tk.Frame(container, bg="#ffffff")
        table_frame.pack(padx=12, pady=8, fill="both", expand=True)

        cols = ("id","nombre","sexo","correo","creado_en")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="w", width=140 if c!="id" else 60)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botón Cerrar que se mueve aleatoriamente
        self.close_btn = tk.Button(container, image=self.btn_imgs["close"], bd=0, cursor="hand2")
        self.close_btn.place(x=700, y=450)  # posición inicial
        # cuando el mouse entra, el botón se mueve
        self.close_btn.bind("<Enter>", self.evade_close)

    # --- Hover effect: sustituye imagen por versión con sombra más fuerte ---
    def add_hover_effect(self, widget, key):
        def on_enter(e):
            # crear versión con sombra más marcada
            img = create_rounded_button_image(
                text=widget.cget("image") and "",  # no usamos texto aquí
                width=self.btn_imgs[key].width(),
                height=self.btn_imgs[key].height(),
                radius=22,
                base_color=(0,0,0),
                shadow=True,
                font_path=self.assets.get("font_path")
            )
            # To keep it simple: slightly enlarge existing image to simulate effect
            widget.config(relief="flat")
            widget.configure(highlightthickness=0)
        def on_leave(e):
            pass
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    # --- Funciones CRUD y nuevas funciones ---
    def add_employee(self):
        nombre = self.entry_nombre.get().strip()
        sexo_raw = self.entry_sexo.get().strip()
        correo = self.entry_correo.get().strip()

        if not nombre or not sexo_raw or not correo:
            messagebox.showwarning("Advertencia", "Rellena todos los campos.")
            return

        sexo_upper = sexo_raw.upper()
        if sexo_upper.startswith("M"):
            sexo_char = "M"
        elif sexo_upper.startswith("F"):
            sexo_char = "F"
        else:
            sexo_char = "O"

        try:
            self.manager.add_employee(nombre, sexo_char, correo)
            self.refresh_employees()
            messagebox.showinfo("Éxito", "Empleado agregado.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_sexo.delete(0, tk.END)
            self.entry_correo.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar empleado:\n{e}")

    def refresh_employees(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            rows = self.manager.list_employees()
            for r in rows:
                self.tree.insert("", "end", values=r)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener empleados:\n{e}")

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un empleado.")
            return
        emp_id = self.tree.item(sel[0], "values")[0]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar empleado ID {emp_id}?")
        if not confirm:
            return
        try:
            ok = self.manager.delete_employee(int(emp_id))
            if ok:
                messagebox.showinfo("Éxito", "Empleado eliminado.")
            else:
                messagebox.showwarning("No encontrado", "Empleado no encontrado.")
            self.refresh_employees()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

    def export_csv(self):
        try:
            filename = self.manager.export_all_to_csv("empleados_export.csv")
            messagebox.showinfo("Exportado", f"Exportado a: {os.path.abspath(filename)}")
            # Abrir carpeta que contiene el archivo (Windows + otros)
            folder = os.path.dirname(os.path.abspath(filename))
            webbrowser.open(folder)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

    # --- Ventana Hola Mundo con GIF animado ---
    def open_message_window(self):
        if "saludo_gif" not in self.assets:
            messagebox.showwarning("Sin GIF", "No se encontró 'saludo.gif' en la carpeta del proyecto.")
            return
        top = tk.Toplevel(self.master)
        top.title("Hola Mundo")
        top.geometry("400x300")
        lbl = tk.Label(top)
        lbl.pack(expand=True)
        # Cargar GIF frames
        gif = Image.open(self.assets["saludo_gif"])
        frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((300,200), Image.LANCZOS)) for frame in ImageSequence.Iterator(gif)]
        def animate(idx=0):
            lbl.config(image=frames[idx])
            top.after(120, animate, (idx+1) % len(frames))
        animate()

    # --- Botón Cerrar que se mueve aleatoriamente cuando entras con el mouse ---
    def evade_close(self, event):
        w = self.master.winfo_width()
        h = self.master.winfo_height()
        # calcular nueva posición dentro de ventana
        new_x = random.randint(20, max(20, w-120))
        new_y = random.randint(60, max(60, h-80))
        self.close_btn.place(x=new_x, y=new_y)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Registro de Empleados - Versión Mejorada")
    app = Application(master=root)
    root.mainloop()
