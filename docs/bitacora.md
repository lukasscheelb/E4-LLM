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

## Revisión de consistencia y trazabilidad · 2026-11-21

- **Actividad:** se cotejaron P-01 a P-09 con la especificación y la historia en la rama de preparación, que partió de `8e77355`. Se precisaron entradas, salidas, flujos alternativos y errores y se añadió la matriz RF/RNF–CA–preguntas.
- **Criterios:** se fijaron valores para mínimos, bandas y errores. Se añadieron CA-15 a CA-17 para los extremos del dominio, la concurrencia de señales sin fraude y los valores numéricos fuera de rango.
- **Pendientes:** se conservaron P-05.a y P-05.b. Se agregó P-07.a para confirmar la precisión de las señales numéricas individuales. Las nueve respuestas acordadas y las referencias a E3 se conservaron.
- **Verificación documental:** se cotejaron los ocho requisitos y los diecisiete criterios en ambos sentidos y se comprobó la conservación de las nueve respuestas acordadas, los enlaces locales y las referencias a E3.
- **Estado:** revisión documental asistida por Codex. Pendiente de aclaración y aprobación expresa. Durante esta revisión no se ejecutaron Developer, el flujo multiagente, las Skills del proyecto ni pytest.

## Cierre documental de las aclaraciones

- **Aceptación expresa:** «Acepto P-05.a, P-05.b y P-07.a tal como están formuladas». La declaración se registró en el chat de trabajo de E4. El representante del cliente es Lukas Scheel.
- **Cambios:** se actualizaron el registro de respuestas, la especificación, CA-12, CA-13, CA-17 y la matriz de trazabilidad. El README refleja que las aclaraciones se cerraron y la aprobación de la revisión quedó pendiente.
- **Verificación documental:** se contrastaron los ocho requisitos y los 17 criterios con el registro de respuestas y se cotejó la distinción entre señal numérica ausente, indicador de fraude omitido y valor inválido.
- **Estado:** queda pendiente la aprobación expresa del commit documental. En esta actualización no se implementó el evaluador ni se ejecutaron Developer, pytest, las Skills del proyecto o el flujo multiagente.

## Verificación de la aprobación previa

- **Decisión humana:** Lukas Scheel aprobó la especificación y la historia del commit [`2c625d6`](https://github.com/lukasscheelb/E4-LLM/commit/2c625d6446b6fdba4cdc361c77f71235c4c4b45e). El commit independiente [`cadb048`](https://github.com/lukasscheelb/E4-LLM/commit/cadb048819b191eac705be26ddae2575986139f9) registró la aprobación y su procedencia. El representante confirmó que este registro satisface el requisito de la pauta.
- **Parentesco en Git:** `git rev-parse cadb048^` devolvió `2c625d6446b6fdba4cdc361c77f71235c4c4b45e`. Tras sincronizar la rama, `git merge-base --is-ancestor cadb048 HEAD` devolvió código 0.
- **Alcance:** `git diff-tree --no-commit-id --name-status -r cadb048` mostró un único archivo modificado, `docs/bitacora.md`. El diff de la especificación, la historia y las preguntas entre la revisión aprobada y `HEAD` estuvo vacío.
- **Orden de ejecución:** `git log --all --format= --name-only` mostró documentación y recursos de agentes y Skills. El único archivo Python del historial era el script reutilizable de `pytest-runner`. La rama estaba limpia antes de preparar la guía. El registro de aprobación precede a cualquier código o prueba del evaluador en el historial inspeccionado.
- **Estado observado:** se verificó Git y se preparó el inicio de la corrida en VS Code. El envío inicial a Analista y la ejecución de agentes, Skills y pytest están pendientes.

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

## Aprobación expresa del representante · 2026-11-21

- **Representante del cliente:** Lukas Scheel.
- **Fecha de aprobación:** 2026-11-21, America/Santiago. La hora exacta del mensaje no está disponible en el contexto del chat.
- **Fecha y hora de transcripción:** 2026-11-21 17:03:58, America/Santiago (20:03:58 UTC).
- **Evidencia:** mensaje del representante en el chat de Codex asociado a este repositorio.
- **Declaración literal:**

  > Como representante del cliente, apruebo expresamente la especificación y la historia de usuario de MIRA E4 en el commit 2c625d6446b6fdba4cdc361c77f71235c4c4b45e.

- **Revisión documental aprobada:** `2c625d6446b6fdba4cdc361c77f71235c4c4b45e`.
- **Documentos de esa revisión:**
  - `docs/trabajo/especificacion.md`
  - `docs/trabajo/historia-usuario.md`
  - `docs/trabajo/preguntas-cliente.md`
- **Decisiones incorporadas:** P-01 a P-09 y aclaraciones P-05.a, P-05.b y P-07.a, con las respuestas y su aceptación registradas en `docs/trabajo/preguntas-cliente.md`.
- **Autorización posterior para el registro y commit:** el representante indicó literalmente «hazlo por mi en mi nombre», después de recibir las instrucciones para registrar la aprobación en un commit independiente que modificara únicamente `docs/bitacora.md`.
- **Procedencia del registro:** decisión y autorización humanas de Lukas Scheel; transcripción y ejecución material del commit realizadas por Codex por encargo expreso. No se afirma que una persona haya ejecutado los comandos de Git. Esta autorización sustituye, para este registro, la ejecución manual solicitada anteriormente.
- **Verificación previa:** el repositorio estaba limpio y HEAD coincidía con la revisión aprobada. El commit dedicado debe incluir únicamente este archivo; su hash se obtiene de Git después de crearlo.
- **Estado al registrar:** aprobación expresa otorgada antes de cualquier implementación. En esta actividad no se ejecutaron los agentes Analista, Planificador, Developer o Reviewer, las Skills del proyecto ni pytest; no se generaron resultados de pruebas, métricas o fallas MAST.

## Corrida multi-r0 · Analista y Planificador · 2026-11-21

- **Encargo humano literal:** «perfecto, quiero que hagas los 7 pasos que quedan por desarrollar. Puedes tomar control de mi pc».
- **Rama y revisión inicial:** `codex/preparacion-e4`, `dba62c90a3c4f3c8b2476a0632b3129aeade182d`; árbol limpio antes del inicio.
- **Aprobación verificada:** `cadb048819b191eac705be26ddae2575986139f9` es ancestro de HEAD y modifica únicamente esta bitácora; no hubo cambios en `docs/trabajo/` respecto de la revisión aprobada `2c625d6446b6fdba4cdc361c77f71235c4c4b45e` antes de iniciar.
- **Herramienta real:** subagentes separados de Codex, no perfiles ejecutados por GitHub Copilot/VS Code. Los perfiles del repositorio se consultaron y siguieron por instrucciones. No se afirma aplicación técnica de los permisos `tools` de VS Code. Modelo y versión exactos no expuestos por estas herramientas.
- **Analista:** subagente `/root/analista`, aplicó `generar-criterios` y su plantilla a los 17 CA. Entregó `docs/trabajo/analisis.md`; prompt íntegro, lecturas, fuente de aprobación y límites constan en `docs/evidencia/multi-r0-analista.md`.
- **Traspaso real Analista → Planificador:** el coordinador leyó el análisis y despachó al subagente `/root/planificador` con referencia explícita al archivo; este lo leyó. Es un traspaso automático autorizado por el encargo, no un envío manual de Copilot ni una intervención humana adicional. Esta ejecución difiere de los botones manuales descritos en la guía y se declara esa diferencia.
- **Planificador:** consultó perfil y `verificar-trazabilidad` con su matriz. Devolvió el plan por respuesta sin escribir archivos; el coordinador lo guardó en `docs/trabajo/plan.md` (normalización de espacios finales). Incluye contrato, diseño y matriz de los 17 CA con código/resultados pendientes. Prompt y mensajes conservados en `docs/evidencia/multi-r0-planificador.md`.
- **Hallazgo y complemento:** el catálogo íntegro no estaba incluido en los documentos E4. El coordinador localizó una copia E3 y Planificador la leyó en un turno posterior. Se anexó su addendum de propuesta de seis señales opcionales, pendiente de decisión del representante. No se cambió la especificación aprobada ni se afirmó equivalencia de la copia con el commit fuente citado.
- **Entorno sin red:** Docker CLI disponible, daemon no activo según comprobación real. CA-10 continúa pendiente; no se deshabilitó la red del equipo.
- **Tiempos:** observaciones parciales con UTC y America/Santiago en las evidencias; no hay medición completa de duración ni tokens. No se convierten estas observaciones en métricas comparativas.
- **Control humano:** se presenta el plan concreto y su addendum al representante para revisión y autorización de Developer. Ese control sigue pendiente; la solicitud general de ejecutar el flujo no se registra como aprobación anticipada de este plan.
- **Estado:** pasos 1, 2 y 3 realizados; Developer, pytest, Reviewer y línea base no iniciados. No se inventaron resultados, correcciones humanas ni fallas MAST. La limitación de catálogo y la indisponibilidad de Docker no se clasificaron como MAST sin evidencia causal suficiente.
- **Evidencia de coordinación:** `docs/evidencia/multi-r0-coordinacion.md`.

## Control humano del plan · 2026-11-21

- **Representante:** Lukas Scheel.
- **Revisión revisada y aprobada:** `30c7d65565f5517a629a09eef258e23c2d6ef743`, `docs/trabajo/plan.md`, incluido el addendum de catálogo presentado en el mensaje anterior.
- **Respuesta literal:** «apruebo, continua».
- **Evidencia:** respuesta del representante en este chat a la solicitud explícita de aprobar el plan, su addendum y autorizar Developer.
- **Decisión humana:** acepta el contrato técnico, diseño y matriz del plan, y las seis señales numéricas adicionales como opcionales (enteros 0–100, validadas y desglosadas, sin mínimos ni efecto en ruta/puntaje); autoriza pasar a Developer.
- **Procedencia:** transcripción por Codex de la decisión humana; no se atribuye al asistente la aprobación. La hora exacta del mensaje no está expuesta; registro observado a las 2026-11-21 20:40:27 UTC / 17:40:27 America/Santiago.
- **Alcance:** se conserva la revisión documental `2c625d6` y su registro `cadb048`; el addendum aprobado se registra como decisión posterior común a la corrida multiagente y a la línea base.
