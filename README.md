# MIRA · Entregable 4

**Alternativa A · Desarrollo conducido por especificación.** El caso propone un evaluador independiente de MIRA que considera puntaje de confianza, señales de fraude y umbrales configurables por organización. El futuro componente será local, en Python y verificable con pytest.

**Estado actual:** Lukas Scheel aprobó la revisión documental. El registro de aprobación precede a la implementación y la primera corrida en VS Code está preparada.

| Documento | Contenido |
|---|---|
| [Historia de usuario](docs/trabajo/historia-usuario.md) | Criterios Given/When/Then |
| [Especificación para revisión](docs/trabajo/especificacion.md) | Fuentes de E3, caso de uso y requisitos |
| [Preguntas al representante](docs/trabajo/preguntas-cliente.md) | Nueve respuestas y tres aclaraciones aceptadas |
| [Decisión de coordinación](docs/decision.md) | Patrón, agentes, herramientas y Skills |
| [Bitácora](docs/bitacora.md) | Actividades observadas y plantillas de registro y aprobación |
| [Evidencia](docs/evidencia/README.md) | Nombres y procedencia de los artefactos |
| [Línea base](docs/linea-base/README.md) | Comparación con un agente generalista |

## Primera corrida multiagente en VS Code

**Revisión aprobada:** `2c625d6446b6fdba4cdc361c77f71235c4c4b45e`. **Registro de aprobación:** `cadb048819b191eac705be26ddae2575986139f9`. Lukas Scheel aprobó la revisión y autorizó a Codex a registrar su declaración. La [bitácora](docs/bitacora.md) documenta la procedencia y la comprobación de Git.

1. Abre la raíz de E4 en la rama `codex/preparacion-e4` actualizada. Inicia sesión en GitHub Copilot, abre Chat y usa **Chat: Open Customizations** para localizar los cuatro agentes y las tres Skills del workspace.
2. Inicia una sesión **Local**, si está disponible, para usar los botones de handoff. Cada botón prepara el mensaje y la persona lo revisa y pulsa **Enviar**. Si usas una sesión **Copilot** que lista los agentes pero carece de esos botones, selecciona manualmente al siguiente agente y pega el prompt del handoff con sus referencias. Registra cuál variante usaste. [Agentes personalizados](https://code.visualstudio.com/docs/agent-customization/custom-agents).
3. Elige **analista** y envía el prompt inicial que aparece abajo. Invoca `generar-criterios` desde el selector de Skills si está disponible. Si no aparece, adjunta su `SKILL.md` y `references/criterio.md` y pide que aplique el procedimiento. Distingue en la bitácora una carga de Skill observada de una consulta explícita de sus archivos. [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills).

### Prompt inicial para analista

> Verifica la historia, la especificación y las decisiones P-01 a P-09 y sus tres aclaraciones en `docs/trabajo/`. Usa la revisión aprobada `2c625d6446b6fdba4cdc361c77f71235c4c4b45e` y el registro `cadb048819b191eac705be26ddae2575986139f9`. Aplica `generar-criterios` y su plantilla a los 17 criterios Given/When/Then. Entrega en el chat un informe con fuentes, criterios revisados, hallazgos y la recomendación de traspaso. Preserva los documentos aprobados. Si un hallazgo cambia una regla o un resultado esperado, documenta la pregunta y detén el traspaso.

### Handoffs y evidencia

Usa un identificador de corrida, por ejemplo `multi-01`. Conserva en `docs/evidencia/` la transcripción o los extractos verificables de cada etapa y el mensaje exacto de cada traspaso. Registra en `docs/bitacora.md` el agente y destino de sesión, modelo, hashes, prompt literal, Skill y recurso utilizados, quién autorizó o envió cada handoff, resultado y enlace al artefacto. Registra horarios, métricas e incidentes MAST solo cuando haya datos observados que los respalden.

| Etapa | Acción y evidencia |
|---|---|
| Analista → Planificador | Guarda el informe de Analista y la evidencia de cómo aplicó `generar-criterios`. La persona comprueba que se preservaron los documentos aprobados y revisa los hallazgos. Si permiten avanzar, envía el handoff con ambos hashes, el informe y las rutas aprobadas. |
| Planificador → Developer | Pide diseño técnico, tareas y matriz de los ocho requisitos y 17 criterios con `verificar-trazabilidad`. Guarda su salida Markdown en `docs/trabajo/plan.md` tras revisarla. Conserva la evidencia del uso de la Skill y envía el handoff con el plan, los hashes y cualquier decisión humana registrada. |
| Developer → Reviewer | Pide verificar que el registro de aprobación sea ancestro de `HEAD` y que los documentos aprobados coincidan con su revisión. Luego debe implementar el evaluador local en Python y ejecutar `pytest-runner`. Guarda comando literal, intérprete y versión de pytest, salida, código de retorno, conteos e informe JUnit si se generó. Adjunta la matriz, el hash o diff reproducible del código probado, y el mensaje de traspaso a Reviewer. |
| Reviewer → cierre o corrección | Comprueba que Reviewer disponga solo de lectura y búsqueda. La persona guarda el veredicto que el agente entrega por chat con las referencias a requisitos, código y evidencia. Tras un rechazo, la persona puede enviar la devolución a Developer hasta dos veces. Registra la primera revisión como inicial y las correcciones como ciclos 1 y 2. Ante un nuevo rechazo tras el ciclo 2, eleva los hallazgos a la persona responsable. |

Si durante la corrida cambia un comportamiento aprobado, vuelve al representante antes de implementar ese cambio. La primera corrida comienza cuando la persona envía el prompt a Analista desde VS Code.
