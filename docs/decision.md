# Decisión de coordinación · Entregable 4

**Patrón elegido:** flujo secuencial con traspasos manuales.

`Analista → aprobación humana → Planificador → Developer → Reviewer`

El insumo de cada etapa es el artefacto de la anterior. Ante fuentes contradictorias, fijar primero una revisión aprobada evita diseñar o programar contra reglas supuestas. Los traspasos manuales permiten comprobar esa referencia antes de avanzar y contar las intervenciones. La revisión de solo lectura deja un veredicto atribuible a una revisión concreta.

Se descartó el patrón orquestador porque el trabajo tiene dependencias principalmente lineales y la decisión central pertenece al representante. Un coordinador automático necesitaría el mismo punto de aprobación, agregaría decisiones de enrutamiento y haría más difícil atribuir tiempo e intervenciones a cada etapa. El representante ya aprobó la revisión. Como control humano adicional, la persona operadora revisa el plan de Planificador y registra si autoriza el paso a Developer o devuelve el plan para corregir. La persona envía los traspasos. Cada traspaso tiene `send: false`. Tras el rechazo de la primera revisión se admiten dos ciclos Developer–Reviewer.

## Agentes y herramientas

| Agente | Responsabilidad | Herramientas y propósito |
|---|---|---|
| [Analista](../.github/agents/analista.agent.md) | Contrastar fuentes, redactar el caso y elevar las preguntas. | `read` para consultar fuentes y artefactos, `search` para localizar referencias y `edit` para actualizar borradores y registrar actividad. |
| [Planificador](../.github/agents/planificador.agent.md) | Diseñar el componente y las pruebas desde el insumo aprobado. | `read` y `search` para la revisión documental. Entrega el plan en Markdown por chat y la persona lo guarda. |
| [Developer](../.github/agents/developer.agent.md) | Implementar, verificar el commit de aprobación y ejecutar las pruebas. | `read` y `search` para consultar el plan y el cambio, `edit` para código, pruebas y registros y `execute` para Git y pytest. |
| [Reviewer](../.github/agents/reviewer.agent.md) | Contrastar requisitos, implementación y evidencia y devolver un veredicto. | `read` y `search` para consultar el cambio y los resultados provistos. La persona guarda el veredicto. |

La configuración usa los alias de VS Code y el destino `vscode` para los botones de Local. La selección manual cubre sesiones Copilot que cargan los agentes sin esos botones. Ningún perfil tiene herramienta de delegación. [Referencia oficial de archivos de agentes](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference).

## Skills reutilizables

| Skill | Técnica y recurso | Uso previsto |
|---|---|---|
| [generar-criterios](../.github/skills/generar-criterios/SKILL.md) | Plantilla de criterios, fronteras y colisiones observables. | Analista |
| [verificar-trazabilidad](../.github/skills/verificar-trazabilidad/SKILL.md) | Matriz bidireccional de requisitos, diseño, código y pruebas. | Planificador y Reviewer. Developer puede completar las referencias de la matriz. |
| [pytest-runner](../.github/skills/pytest-runner/SKILL.md) | Script Python que invoca pytest con el mismo intérprete, devuelve el código de salida y admite JUnit. | Developer |

El criterio de avance es la evidencia de la etapa anterior. Para la comparación académica, se congela la revisión aprobada y se aplica el mismo protocolo de verificación a ambos enfoques. [Metodología](linea-base/README.md).
