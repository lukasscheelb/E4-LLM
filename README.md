# MIRA · Entregable 4

**Equipo:** Lukas Scheel (representante de negocio), Francisca Meyer y Sebastian Rodriguez.

**Entrega académica:** [informe PDF](output/pdf/Informe_MIRA_E4.pdf), [presentación PowerPoint](output/presentacion/Presentacion_MIRA_E4.pptx), [guion de demostración](docs/entrega/guion-demo.md) y [estado y límites de entrega](docs/entrega/README.md). Diagrama y tabla de agentes en `docs/entrega/`. La versión final se identifica mediante la etiqueta `entrega-3`. Los puntos que requieren una respuesta o actuación humana se declaran pendientes, sin dar por completado un ensayo ni métricas inexistentes.

**Alternativa A · Desarrollo conducido por especificación.** El caso propone un evaluador independiente de MIRA que considera puntaje de confianza, señales de fraude y umbrales configurables por organización. El componente es local, en Python y verificable con pytest.

**Entrada del caso:** el cliente necesita que MIRA use el puntaje del caso, las señales de fraude y los umbrales de cada organización para decidir la ruta y explicar el motivo. El comportamiento exacto está en la especificación aprobada.

**Estado actual:** revisión documental y plan aprobados por Lukas Scheel; implementación y pruebas reales completadas mediante subagentes separados de Codex. Suite propia: 173/173; suite común de aceptación: 115/115, con aislamiento de red verificado en Docker. Veredicto independiente en [la revisión](docs/trabajo/revision.md) y [comparación con un generalista](docs/linea-base/comparacion.md).

La corrida entregada utilizó Codex, siguiendo los perfiles del repositorio por instrucciones; no se presenta como una corrida de GitHub Copilot/VS Code. Los traspasos entre subagentes fueron coordinados automáticamente, con aprobación humana previa de la especificación y control humano adicional del plan. La guía VS Code de abajo se conserva como alternativa de reproducción, no como evidencia de esa herramienta.

| Documento | Contenido |
|---|---|
| [Análisis ejecutado](docs/trabajo/analisis.md) | Revisión de los 17 criterios mediante generar-criterios |
| [Plan aprobado](docs/trabajo/plan.md) | API, diseño, pruebas y addendum de catálogo |
| [Implementación](docs/trabajo/implementacion.md) | Trazabilidad, pruebas y ejecución sin red |
| [Revisión independiente](docs/trabajo/revision.md) | Veredicto de Reviewer de solo lectura |
| [Historia de usuario](docs/trabajo/historia-usuario.md) | Criterios Given/When/Then |
| [Especificación para revisión](docs/trabajo/especificacion.md) | Fuentes de E3, caso de uso y requisitos |
| [Preguntas al representante](docs/trabajo/preguntas-cliente.md) | Nueve respuestas y tres aclaraciones aceptadas |
| [Decisión de coordinación](docs/decision.md) | Patrón, agentes, herramientas y Skills |
| [Bitácora](docs/bitacora.md) | Actividades observadas y plantillas de registro y aprobación |
| [Evidencia](docs/evidencia/README.md) | Nombres y procedencia de los artefactos |
| [Línea base](docs/linea-base/README.md) | Comparación con un agente generalista |

## Ejecutar la Alternativa A en VS Code

La especificación de `2c625d6` ya fue aprobada por Lukas Scheel. El commit independiente `cadb048` registra su decisión. [Bitácora](docs/bitacora.md).

Abre el repositorio en `codex/preparacion-e4` y abre GitHub Copilot Chat. En **Chat: Open Customizations** ubica los agentes y las Skills del proyecto. Selecciona **Local** para usar los botones de traspaso. Cada botón prepara el mensaje con `send: false`. Revisa que cite el archivo de trabajo y envíalo. Si tu sesión Copilot lista los agentes sin botones, selecciona manualmente al siguiente agente y envía el mismo mensaje con el archivo. [Agentes y handoffs en VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents#handoffs).

En el campo de chat, escribe `/` para seleccionar la Skill de la etapa cuando esté disponible. Guarda una captura o el registro de actividad que muestre su carga y uso real. [Skills en VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills#use-skills-as-slash-commands).

| Agente que seleccionas | Mensaje y archivo que debe quedar |
|---|---|
| **analista** | «A partir de la necesidad del cliente descrita al inicio del README, usa `generar-criterios` y su plantilla para revisar los 17 criterios de la historia aprobada en `2c625d6`. Usa las respuestas registradas, conserva los documentos aprobados y guarda tu análisis y sus referencias en `docs/trabajo/analisis.md`». |
| **planificador** | «Lee `docs/trabajo/analisis.md`, la especificación aprobada y su registro `cadb048`. Usa `verificar-trazabilidad` para diseñar las tareas, la API mínima en Python y las pruebas por criterio. Devuelve el plan en Markdown». Guarda el texto entregado por el agente en `docs/trabajo/plan.md`. **Control humano adicional:** revisa el plan y registra en la bitácora qué revisaste y si autorizas el paso a Developer o devuelves una corrección. |
| **developer** | «Lee `docs/trabajo/plan.md`. Verifica en Git que `cadb048` precede a la implementación. Implementa el evaluador en `src/` con una API Python invocable y sus pruebas en `tests/`, sin Bonsai. Ejecuta el script de la Skill `pytest-runner`. Guarda el resumen, la revisión probada y el enlace a la salida real en `docs/trabajo/implementacion.md`». |
| **reviewer** | «Lee `docs/trabajo/implementacion.md`, el plan, la revisión aprobada y la evidencia de pytest. Revisa la trazabilidad y devuelve un veredicto en el chat». Verifica que el perfil solo tenga lectura y búsqueda. Guarda su texto en `docs/trabajo/revision.md`. Si rechaza, envía ese archivo a Developer para corregir. El límite es de dos ciclos de corrección. |

El equipo guarda las salidas del Planificador y del Reviewer tal como se produjeron. Para cada etapa, registra en [la bitácora](docs/bitacora.md) el prompt literal, el traspaso, la decisión humana que corresponda y el enlace a la evidencia. En `docs/evidencia/` conserva las capturas o salidas del chat, el uso de las tres Skills y la salida real de pytest. El registro de prueba debe identificar el código probado y el resultado. Si el equipo rechaza o corrige una salida, conserva el cambio y la nueva ejecución que realmente ocurra.

## Comparación y entrega

Ejecuta también la [línea base](docs/linea-base/README.md) con un solo agente en una rama separada, desde la misma revisión previa al código. Completa la tabla con los datos reales de ambas corridas.

Cuando el flujo esté completo, pytest esté en verde, Reviewer haya aprobado y la comparación esté guardada, integra la versión verificada en `main` conservando los commits. La pauta pide la etiqueta `entrega-3` para la demostración. Colócala sobre la versión final y usa esa versión en la demo.

## Usar el evaluador local

La implementación fue aprobada por Reviewer y CA-10 tiene evidencia real de ejecución sin red. Véanse el [veredicto](docs/trabajo/revision.md) y la [comparación](docs/linea-base/comparacion.md).

Requiere Python 3.10 o superior. En PowerShell, desde la raíz:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe .github/skills/pytest-runner/scripts/run_pytest.py tests
```

La API es `from mira import evaluar_caso`. En una sesión Python iniciada con `src/` en `PYTHONPATH`:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
.\.venv\Scripts\python.exe
```

```python
from mira import evaluar_caso

caso = {
    "organizacion": "X", "puntaje": 85,
    "senales": {
        "DOC_AUT": 70, "BIO_ROSTRO": 75,
        "CRUCE_MONTO": 60, "CRUCE_FECHA": 60,
        "FRA_EDICION": False, "FRA_MEMORIA": False, "FRA_SINTETICO": False,
    },
}
configuraciones = {"X": {"id": "config-X", "version": "1", "R": 60, "A": 85}}
resultado = evaluar_caso(caso, configuraciones)
print(resultado["decision"])  # APROBACION_AUTOMATICA
```

La función devuelve diccionarios con `ok`, decisión, motivos, puntaje, desglose y configuración. Ante un dato inválido devuelve `ok=False` y `error`, sin decisión. No calcula puntajes ni accede a Bonsai o servicios. Las seis señales numéricas opcionales del addendum aprobado se validan y desglosan cuando llegan, sin mínimos ni efecto en la ruta. Véanse el [plan](docs/trabajo/plan.md) y la [evidencia de implementación](docs/trabajo/implementacion.md).
