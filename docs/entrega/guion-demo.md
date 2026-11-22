# Guion de presentación y demostración

## Reparto propuesto de 15 minutos

| Diapositiva | Persona | Segundos |
|---|---|---:|
| 1 Portada | Lukas | 40 |
| 2 Caso | Lukas | 80 |
| 3 Roles y archivos | Francisca | 75 |
| 4 Skills | Francisca | 60 |
| 5 Aprobaciones | Francisca | 45 |
| 6 Demostración | Sebastian | 360 |
| 7 Resultados | Sebastian | 60 |
| 8 Incidencias | Francisca | 50 |
| 9 Discusión | Lukas | 80 |
| 10 Aprendizajes | Sebastian | 50 |
| **Total** | **Todo el equipo** | **900** |

Es una asignación propuesta, no un ensayo realizado. Todos deben poder responder sobre cualquier parte. Reservar cinco minutos adicionales para preguntas, según la pauta.

## Preparación anterior a la exposición

1. Obtener la etiqueta `entrega-3` en un clon o checkout limpio. No hacer checkout sobre cambios propios sin guardarlos.
2. Preparar Python 3.10 o superior y las dependencias de `requirements-dev.txt`. La instalación inicial puede necesitar red; hacerla antes de la demostración.
3. Abrir README, `analisis.md`, `plan.md`, bitácora, implementación y revisión. Dejar visibles las referencias cadb048 y 5a7b12d.
4. Preparar Docker Desktop si se mostrará aislamiento. La imagen `mira-e4-pytest:9.0.2` se construye previamente desde `docs/evidencia/Dockerfile.pruebas`. No descargar dependencias durante el tramo sin red.
5. Abrir el PPTX y practicar transiciones. Esta preparación no acredita un ensayo oral.

## Demostración de seis minutos

- 0:00–0:50: mostrar necesidad y revisión documental aprobada. Identificar la decisión humana, no solo un archivo modificado.
- 0:50–1:40: mostrar análisis, skill usada, plan y autorización humana del plan.
- 1:40–3:10: ejecutar `python scripts/demo.py`. Muestra 84/85/59, colisión de fraude/mínimo/ausencia y un indicador omitido. Explicar por qué un error no produce decisión.
- 3:10–4:10: ejecutar `python .github/skills/pytest-runner/scripts/run_pytest.py tests`. Mostrar retorno y correspondencia con archivos. En un entorno preparado tarda segundos.
- 4:10–5:00: mostrar `cierre-multi-entorno.json` y `docker-inspect`: red none, solo lo, sin ruta externa. Si se repite, usar un contenedor nuevo y guardar el nuevo log, sin sobrescribir evidencia histórica.
- 5:00–6:00: mostrar `revision.md` y comparación 115/115, con límites experimentales.

`demo.py` reproduce el producto, no ejecuta cuatro agentes. Para la condición de agentes en vivo, lanzar Analista con su perfil/skill sobre una copia de demostración, mostrar su carga y un traspaso; si todo el flujo excede seis minutos, mostrar finales de la corrida guardada coherentes con la versión entregada, como permite la pauta. No sustituir la corrida real por un guion narrado. No fingir una aprobación humana nueva ni registrar un rechazo que no haya ocurrido.

## Preguntas para preparar entre los tres

- ¿Por qué fraude no resta puntaje y por qué el rechazo es humano?
- ¿Qué diferencia hay entre ausencia numérica e indicador de fraude omitido?
- ¿Cómo se desempatan motivos concurrentes?
- ¿Por qué Reviewer no edita ni ejecuta pruebas?
- ¿Qué contiene el manifiesto y cómo afecta CRLF/LF?
- ¿Por qué 173 pruebas frente a 124 no demuestra superioridad?
- ¿Qué métricas faltan y cómo se medirían en otra corrida?
- ¿Qué parte de la clasificación MAST es interpretación?

## Registro de ensayo a completar por el equipo

Fecha, participantes, inicio y fin, duración por bloque, error observado y ajuste. Se deja vacío deliberadamente: no hay evidencia de un ensayo oral realizado por los tres.
