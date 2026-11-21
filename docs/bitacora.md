# Bitácora · Entregable 4

## Registro inicial · 2026-11-21

- **Actividad real:** preparación documental asistida por Codex. Se consultaron los archivos de la copia local de E3 y la documentación oficial de VS Code, se creó la rama de preparación y se redactaron el flujo y la especificación. Las fuentes consultadas quedan identificadas en [la especificación](trabajo/especificacion.md).
- **Encargo recibido:** el prompt completo de preparación está en el adjunto `Texto pegado.txt` del chat. Para la comparación se conservarán los prompts literales enviados durante las corridas, incluidos los textos de los traspasos.
- **Incidencias de preparación:** el acceso por Git a GitHub falló por resolución de red. Se usaron la copia local de E3 y el conector de GitHub para verificar la referencia y el estado vacío de E4. La creación local de la rama necesitó permiso para escribir en `.git`.
- **Verificación de preparación:** se validaron los encabezados YAML, los destinos y el envío manual de los traspasos, el acceso de solo lectura del Reviewer y los enlaces locales. El script mostró su ayuda y se comprobó la propagación de los códigos 0, 1 y 5 con un subproceso simulado. Estas verificaciones no ejecutaron pytest ni un flujo de agentes.
- **Estado:** aprobación humana, uso de las Skills del proyecto, ejecución de pytest del componente, flujo multiagente y corrida de línea base pendientes.

## Actualización documental · 2026-11-21

- **Prompt literal:** «vuelve a revisar el repo y actualizalo».
- **Actividad real:** se incorporó mediante avance rápido el commit [`27b67c6`](https://github.com/lukasscheelb/E4-LLM/commit/27b67c6c9ea6c4f931347abc43bdcdb509408f8d) y se trasladaron las nueve respuestas registradas a la especificación y la historia. Se documentaron dos aclaraciones sobre estados de señales.
- **Verificación:** se comprobaron los enlaces locales y las referencias entre ocho requisitos, catorce criterios y las decisiones del representante.
- **Estado:** revisión documental pendiente de aprobación expresa. Esta actualización no es el commit humano de aprobación. El flujo de agentes, las Skills del proyecto y pytest permanecen sin ejecución en esta actualización.

## Plantilla de actividad

Copia por actividad real. Los campos que no apliquen pueden indicarse como tales.

- Fecha, hora y zona:
- ID de corrida, rama y revisión:
- Agente, modelo y etapa:
- Acción humana, motivo y origen → destino del traspaso, si aplica:
- Prompt literal enviado:

  ```text
  <pegar texto exacto>
  ```

- Skills, forma de consulta, recursos realmente usados y evidencia:
- Resultado observado, error, corrección, reintento y evidencia:
- Duración, tokens o aproximación según la metodología:
- Incidente MAST observado, categoría justificada y evidencia, si aplica:

## Plantilla para el registro humano de aprobación

Este bloque se completa únicamente después de recibir aprobación expresa para una revisión específica. Guarda el registro completado en un commit dedicado previo a la implementación. El hash del commit que contiene el registro se puede verificar en Git y se adjunta al traspaso.

- Representante del cliente y rol:
- Fecha, hora y zona de la aprobación:
- Declaración literal o referencia verificable a la aprobación:
- Hash de la revisión aprobada y rutas de historia, especificación y respuestas:
- Preguntas resueltas y evidencia de las respuestas:
- Persona que registra la aprobación:
