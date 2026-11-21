# Entrega académica MIRA E4

## Equipo

- Lukas Scheel, representante de negocio.
- Francisca Meyer.
- Sebastian Rodriguez.

Identificación proporcionada por el usuario. Falta confirmar quién representó al cliente en E2; no se afirma la rotación sin respuesta.

## Instalación desde un equipo nuevo

[Guía paso a paso](guia-instalacion.md) y [PDF descargable](../../output/pdf/Guia_Instalacion_MIRA_E4.pdf).

## Artefactos

- `output/pdf/Informe_MIRA_E4.pdf`: informe de diez páginas con portada y ocho secciones dentro de sus máximos.
- `output/presentacion/Presentacion_MIRA_E4.pptx`: diez diapositivas editables con notas y reparto propuesto de quince minutos.
- `docs/entrega/informe.md` y `contenido.json`: fuentes del informe.
- `docs/entrega/diagrama.mmd`: sistema, archivos, decisiones humanas y correcciones máximas.
- `docs/entrega/agentes.md`: tabla de entradas, salidas, herramientas, término y skills.
- `docs/entrega/fallas.md`: incidentes reales, clasificación interpretativa, causas y límites.
- `docs/entrega/guion-demo.md`: demostración, tiempos, participación y preguntas.
- `scripts/demo.py`: reproducción de cinco casos del producto. Se verificó el proceso; no representa una corrida de agentes.
- `docs/evidencia/cierre-*-junit.xml`: aceptación posterior con guardia del origen de módulo, 115/115 en ambos enfoques.

Los artefactos originales de la corrida, la bitácora y los prompts están en `docs/trabajo/` y `docs/evidencia/`. La línea base original está en la rama `codex/linea-base`, commit 79c69fd.

## Herramienta y versiones

La ejecución multiagente fue Codex Desktop con subagentes separados, siguiendo perfiles por instrucciones. El identificador exacto del modelo y la versión de la app no estuvieron expuestos. El runtime de autoría de documentos fue bundle 26.1119.11507, Python 3.12.14; no es la versión del modelo. Pruebas del producto: Python 3.14.3 local y 3.14.10 Linux; pytest 9.0.2 en la evaluación común; Docker 29.9.2. El generalista usó inicialmente pytest 9.2.0 en su suite Windows; la comparación aislada usó 9.0.2 para ambos.

La edición live de presentaciones falló con `requires MXC in its execution environment`; se creó un PPTX local mediante Artifact Tool. No se afirma que se haya inspeccionado en PowerPoint. Sus diez imágenes renderizadas sí fueron revisadas, junto con las páginas del PDF.

## Reproducción rápida

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/python.exe scripts/demo.py
.venv/Scripts/python.exe .github/skills/pytest-runner/scripts/run_pytest.py tests
```

La guía de flujo de agentes está en el README principal. La instalación depende del entorno y red; no se garantiza un tiempo de descarga. Con dependencias preparadas, la demo del producto es de segundos.

## Mediciones y límites pendientes

La comparación funcional está completa: 17 CA y ocho requisitos, suite común 115/115 en ambos. No existen tiempos totales ni tokens completos medidos con ventanas equivalentes. La ausencia no se reemplaza por cifras inventadas. Debe declararse en el informe o efectuarse otra corrida controlada con instrumentación previa. Las notas de presentación tampoco equivalen a un ensayo humano.

Verificaciones externas pendientes: rotación del representante, acceso real del docente, datos de versión/modelo y confirmación del plazo inconsistente del PDF docente. No se invitó a terceros ni se cambió la visibilidad del repositorio sin identidad/autorización específica.

## Fuentes

Pauta docente local aportada por el usuario; referencias del caso aprobadas en la especificación; [taxonomía MAST, fuente primaria](https://arxiv.org/html/2503.13657v2). La clasificación de los incidentes es interpretativa y sus incertidumbres se declaran.
