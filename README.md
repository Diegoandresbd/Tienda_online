# Glamour Beauty - Proyecto Docker

Este proyecto es una tienda en línea de maquillaje minimalista, desarrollada en Python (Flask) y MySQL. El sistema utiliza **dos contenedores Docker comunicados entre sí** a través de una red interna.

## Tecnologías y Justificación
* **Web (Frontend/Backend):** Python con Flask. Se eligió la imagen oficial `python:3.11-slim` por su ligereza y seguridad.
* **Base de Datos:** MySQL. Se eligió la imagen oficial `mysql:8.0` por su robustez y estabilidad.

## Requisitos previos
* Tener Docker y Docker Compose instalados y en ejecución.

## 🚀 Cómo levantar el proyecto

1. Clonar este repositorio.
2. En la carpeta raíz del proyecto, crear un archivo llamado `.env` y pegar las siguientes variables (puedes cambiar las contraseñas por las tuyas):
   ```env
   MYSQL_ROOT_PASSWORD=root_password_segura
   MYSQL_DATABASE=tienda_online
   MYSQL_USER=usuario_tienda
   MYSQL_PASSWORD=contraseña_segura_tienda
