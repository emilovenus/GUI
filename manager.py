from db import get_connection

class EmployeeManager:
    def add_employee(self, nombre, sexo, correo):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO empleados (nombre, sexo, correo) VALUES (%s, %s, %s)",
            (nombre, sexo, correo)
        )
        conn.commit()
        cur.close()
        conn.close()

    def delete_employee(self, emp_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM empleados WHERE id = %s", (emp_id,))
        conn.commit()
        cur.close()
        conn.close()

    def list_employees(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, sexo, correo FROM empleados")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
