# Sistema de Registro de Empleados en Python

🔹 **Descripción del Proyecto**
Este proyecto implementa un **Sistema de Registro de Empleados** utilizando **Python**, **Tkinter** y **MySQL**, aplicando **Programación Orientada a Objetos (POO)** para mantener un código modular, limpio y escalable.

El sistema permite gestionar de manera sencilla:

- Registro de empleados (con ID generado automáticamente).
- Visualización de todos los empleados registrados.
- Eliminación de empleados desde la interfaz gráfica.
- Conexión directa y segura a la base de datos MySQL.

El programa utiliza una interfaz gráfica construida con **Tkinter**, la biblioteca estándar de Python para crear GUIs, ofreciendo una forma visual e intuitiva de interactuar con la base de datos.

---

🔹 **Estructura del Proyecto**
```
GUI/
│
├── app.py               # Interfaz gráfica principal creada con Tkinter
├── db.py                # Configuración y conexión con la base de datos MySQL
├── manager.py           # Lógica de manejo de empleados (agregar, listar, eliminar)
├── README.md            # Este archivo
└── captura_programa.png # Imagen de la interfaz gráfica en ejecución
```

---

🔹 **Base de Datos**
La base de datos utilizada se llama **empleados_db** y contiene una tabla principal:

**Tabla: empleados**

| id | nombre | sexo | correo |
|----|---------|------|--------|


> 📘 El campo **id** se genera automáticamente al registrar un nuevo empleado.

---

🔹 **Captura de la Interfaz**
La versión final incluye una **interfaz gráfica construida con Tkinter**.  
Agrega aquí una imagen de la ejecución del programa:

**Captura del Sistema**

![Captura del Sistema](./captura_terminal.png)

---

🔹 **Cómo Ejecutar el Proyecto**

1. **Preparar la Base de Datos**
   - Abrir MySQL Workbench o la terminal MySQL.
   - Crear la base de datos y tabla ejecutando:
     ```sql
     CREATE DATABASE empleados_db;
     USE empleados_db;

     CREATE TABLE empleados (
         id INT AUTO_INCREMENT PRIMARY KEY,
         nombre VARCHAR(100),
         sexo VARCHAR(100),
         correo VARCHAR(100)
     );
     ```

2. **Instalar el conector de MySQL para Python**
   ```bash
   pip install mysql-connector-python
   ```

3. **Configurar la conexión en `db.py`**
   ```python
   return mysql.connector.connect(
       host="localhost",
       user="root",
       password="tu_contraseña",
       database="empleados_db"
   )
   ```

4. **Ejecutar el programa**
   ```bash
   python app.py
   ```

---

🔹 **Mejoras Realizadas respecto al código original**
- Implementación de **POO** para una estructura modular.
- Interfaz gráfica completa con **Tkinter**.
- Integración de **MySQL** para persistencia real de los datos.
- Sistema de ID automático.
- Código organizado y legible en archivos separados.
- Uso de consultas seguras para evitar errores y mantener integridad de datos.
