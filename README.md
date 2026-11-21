# MIRA · Entregable 4

**Alternativa A · Desarrollo conducido por especificación.** El caso propone un evaluador independiente de MIRA que considera puntaje de confianza, señales de fraude y umbrales configurables por organización. El futuro componente será local, en Python y verificable con pytest.

**Estado actual:** especificación e historia actualizadas con las respuestas del representante. Las tres aclaraciones de contrato están aceptadas. Está pendiente la aprobación expresa de la revisión documental.

| Documento | Contenido |
|---|---|
| [Historia de usuario](docs/trabajo/historia-usuario.md) | Criterios Given/When/Then |
| [Especificación para revisión](docs/trabajo/especificacion.md) | Fuentes de E3, caso de uso y requisitos |
| [Preguntas al representante](docs/trabajo/preguntas-cliente.md) | Nueve respuestas y tres aclaraciones aceptadas |
| [Decisión de coordinación](docs/decision.md) | Patrón, agentes, herramientas y Skills |
| [Bitácora](docs/bitacora.md) | Actividades observadas y plantillas de registro y aprobación |
| [Evidencia](docs/evidencia/README.md) | Nombres y procedencia de los artefactos |
| [Línea base](docs/linea-base/README.md) | Comparación con un agente generalista |

## Ejecutar el flujo en VS Code

1. Abre la raíz de E4 en la rama de preparación. Inicia sesión en GitHub Copilot y abre Chat. Ejecuta **Chat: Open Customizations** para verificar que aparezcan los cuatro agentes y las tres Skills del workspace.
2. Selecciona **Local** como destino de sesión para usar los botones configurados en `.github/agents/`. Si tu versión solo ofrece **Copilot** y reconoce los agentes, selecciona a cada agente manualmente y pega el texto del `prompt` de su traspaso con las referencias a los archivos y commits. En la sesión de **reviewer**, verifica que el selector de herramientas solo muestre lectura y búsqueda antes de enviar. En Copilot, los botones de `handoffs` de Local no están disponibles. Si la Skill pedida no aparece al escribir `/`, adjunta su `SKILL.md` y su recurso y solicita aplicar el procedimiento documentado. Registra cómo se cargó o consultó. [Agentes personalizados](https://code.visualstudio.com/docs/agent-customization/custom-agents) · [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills).
3. Elige **analista**. Prompt inicial para una futura sesión: «Revisa la historia, la especificación preliminar y las preguntas en `docs/trabajo/` contra las fuentes de E3. Aplica `generar-criterios` a las revisiones que propongas. Registra los puntos pendientes y detente en la revisión humana». Si el agente no puede acceder a E3, adjunta las fuentes citadas. Conserva el texto realmente enviado y la evidencia en la bitácora.
4. Presenta al representante el commit documental que incorpora sus respuestas y las tres aclaraciones aceptadas. Pídele que apruebe expresamente esa revisión por su hash. Una persona transcribe la aprobación y la referencia al commit en la bitácora y crea un **segundo commit independiente** dedicado a la aprobación, antes de cualquier implementación. Para ese segundo commit, usa `git add -- docs/bitacora.md` y comprueba con `git diff --cached --name-only` que solo se incluyó ese archivo. Conserva ambos hashes y facilita al planificador la evidencia de Git y los documentos aprobados. Mientras falte la aprobación, detén el flujo aquí.
5. Selecciona el traspaso a **planificador** y envía el prompt. Cada botón solo prepara el mensaje porque todos usan `send: false`. Revisa el plan, guárdalo en `docs/trabajo/plan.md` y pasa a **developer** con las rutas y los hashes. Developer verifica el prerrequisito, implementa y ejecuta la Skill `pytest-runner` con pytest disponible.
6. Envía a **reviewer** la revisión aprobada, el plan, los archivos o diff y la evidencia de pruebas. Guarda su veredicto desde el chat. Tras un rechazo, se permiten hasta dos ciclos Developer → Reviewer. La primera entrega se registra como revisión inicial, y las correcciones como ciclo 1 y ciclo 2. Tras el último rechazo, escala a la persona responsable. Los botones son sugerencias estáticas, así que la persona controla cuándo enviarlos y registra cada intervención.

Codex se utilizó para preparar los archivos. La guía de traspasos describe GitHub Copilot Chat en VS Code. La etapa actual termina al publicar la revisión documental para aprobación humana.
