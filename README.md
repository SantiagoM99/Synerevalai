<h1 align="center">SynerevalAI</h1>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: Black"></a>
</p>


---

**Synerevalai** es una herramienta diseñada para evaluar y comparar las respuestas generadas por modelos de lenguaje de gran tamaño (LLMs) utilizando múltiples métricas y enfoques. Su objetivo es proporcionar una evaluación multimodal que permita analizar la calidad y eficacia de las respuestas en diversos contextos.

## Aplicaciones y Objetivos

- **Aplicaciones:**
  - Evaluación comparativa de diferentes LLMs en tareas específicas.
  - Análisis detallado de las respuestas generadas para identificar fortalezas y áreas de mejora.
  - Desarrollo de benchmarks personalizados para necesidades particulares de evaluación.
  - Calificación de respuestas de estudiantes en entornos educativos a través de archivos Excel.

- **Objetivos:**
  - Proporcionar una plataforma flexible y extensible para la evaluación de LLMs.
  - Integrar múltiples métricas de evaluación para ofrecer una visión completa del rendimiento de los modelos.
  - Facilitar la comparación objetiva entre diferentes modelos y configuraciones.
  - Permitir la personalización de las métricas y los métodos de evaluación según las necesidades del usuario.

## Configuración Local

Este proyecto está desarrollado en **Python**.

### 1. Clonar el repositorio

```bash
git clone https://github.com/SantiagoM99/Synerevalai.git
cd Synerevalai
```                   

### 2. Crear y activar el entorno virtual

En sistemas Unix:

```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows:

```batch
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo **.env** en la raíz del proyecto con las variables de entorno necesarias, como claves de API o configuraciones específicas. Asegúrate de consultar la documentación o el código fuente para identificar las variables requeridas.

### 5. Ejecutar la aplicación

Para correr el servidor de FastAPI correr el siguiente comando:

```bash
uvicorn src.main:app --reload
```
El servidor estará corriendo `http://127.0.0.1:8000`.

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo [LICENSE](https://github.com/SantiagoM99/Synerevalai/blob/main/LICENSE) para más detalles.
