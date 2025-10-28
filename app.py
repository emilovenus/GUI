import tkinter as tk
from tkinter import ttk, messagebox
from manager import EmployeeManager

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.manager = EmployeeManager()
        self.grid(padx=10, pady=10)
        self.create_widgets()
        self.refresh_employees()

    def create_widgets(self):
        # Formulario
        frm = ttk.LabelFrame(self, text="Añadir empleado")
        frm.grid(row=0, column=0, sticky="ew", pady=5)

        ttk.Label(frm, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = ttk.Entry(frm)
        self.entry_nombre.grid(row=0, column=1)

        ttk.Label(frm, text="Sexo (M/F/O):").grid(row=1, column=0)
        self.entry_sexo = ttk.Entry(frm)
        self.entry_sexo.grid(row=1, column=1)

        ttk.Label(frm, text="Correo:").grid(row=2, column=0)
        self.entry_correo = ttk.Entry(frm)
        self.entry_correo.grid(row=2, column=1)

        ttk.Button(frm, text="Añadir", command=self.add_employee).grid(row=3, column=0, columnspan=2, pady=5)

        # Tabla
        self.tree = ttk.Treeview(self, columns=("id", "nombre", "sexo", "correo"), show="headings")
        for col in ("id", "nombre", "sexo", "correo"):
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=1, column=0, pady=10)

        ttk.Button(self, text="Eliminar seleccionado", command=self.delete_selected).grid(row=2, column=0, pady=5)
        ttk.Button(self, text="Refrescar", command=self.refresh_employees).grid(row=3, column=0, pady=5)

    def add_employee(self):
        nombre = self.entry_nombre.get().strip()
        sexo_raw = self.entry_sexo.get().strip()
        correo = self.entry_correo.get().strip()

        if not nombre or not sexo_raw or not correo:
            messagebox.showwarning("Advertencia", "Rellena todos los campos.")
            return

        # Normalizar el valor de 'sexo' (evita error por texto largo)
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
        for row in self.manager.list_employees():
            self.tree.insert("", "end", values=row)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Selecciona un empleado.")
            return
        emp_id = self.tree.item(sel[0], "values")[0]
        self.manager.delete_employee(emp_id)
        self.refresh_employees()
        messagebox.showinfo("Éxito", "Empleado eliminado.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Registro de Empleados")
    app = Application(master=root)
    app.mainloop()
