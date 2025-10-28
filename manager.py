# manager.py
import csv
from db import get_connection

class EmployeeManager:
    def add_employee(self, nombre, sexo, correo):
        conn = get_connection()
        try:
            cur = conn.cursor()
            sql = "INSERT INTO empleados (nombre, sexo, correo) VALUES (%s, %s, %s)"
            cur.execute(sql, (nombre.strip(), sexo.strip(), correo.strip()))
            conn.commit()
            emp_id = cur.lastrowid
            cur.close()
            return emp_id
        finally:
            conn.close()

    def delete_employee(self, emp_id):
        conn = get_connection()
        try:
            cur = conn.cursor()
            sql = "DELETE FROM empleados WHERE id = %s"
            cur.execute(sql, (int(emp_id),))
            conn.commit()
            affected = cur.rowcount
            cur.close()
            return affected > 0
        finally:
            conn.close()

    def list_employees(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            sql = "SELECT id, nombre, sexo, correo, creado_en FROM empleados ORDER BY id"
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            return rows
        finally:
            conn.close()

    def export_all_to_csv(self, filename="empleados_export.csv"):
        """
        Exporta todos los registros a CSV. Filename se guarda en la carpeta donde se ejecuta el script.
        """
        rows = self.list_employees()
        if not rows:
            # crea archivo vacío con encabezados
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id","nombre","sexo","correo","creado_en"])
            return filename

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id","nombre","sexo","correo","creado_en"])
            for r in rows:
                writer.writerow(r)
        return filename
