# Metodología de comparación con un solo agente

**Estado:** protocolo preparado. Las dos corridas y sus mediciones están pendientes.

## Preparación de la comparación

1. Fija el commit de aprobación del cliente, la revisión asociada y el mismo objetivo de implementación para ambas corridas. Crea dos ramas de experimento desde el commit de aprobación. Inicia dos chats sin historial y mantén el mismo modelo, entorno, versiones, insumos y límites de tiempo o turnos. Registra las diferencias inevitables.
2. Lanza el flujo secuencial en una rama. En la otra, usa un solo agente generalista durante todas las etapas, con permisos de leer, buscar, editar y ejecutar. Entrega la misma especificación aprobada y el mismo encargo. El generalista diseña, implementa, prueba y autoevalúa en su sesión sin delegación ni acceso a productos generados por la otra corrida.
3. Usa el mismo inicio de medición, desde el primer prompt de trabajo posterior a la aprobación compartida, y el mismo fin, cuando la entrega incluye código, pruebas y veredicto o alcanza el límite documentado. La preparación y aprobación previas son comunes y pueden registrarse aparte. Usa un orden fijado antes de comenzar y evita transferir hallazgos entre sesiones.
4. Antes de las corridas, fija una suite común de aceptación y una lista de requisitos basada en la revisión aprobada. Tras cada entrega, aplica ambas al mismo tipo de instantánea. Las suites que escriba cada agente también se reportan, con sus tamaños y resultados propios.

Prompt inicial propuesto para la línea base, que se registrará literalmente al enviarse:

> Con la revisión aprobada y su commit de aprobación adjuntos, diseña, implementa y verifica el evaluador local de MIRA en Python con pytest. Entrega trazabilidad requisito–diseño–código–prueba y una autoevaluación con evidencia. Continúa en este mismo chat sin delegar.

## Registro de medidas

| Métrica | Método | Secuencial | Agente único |
|---|---|---|---|
| Tiempo transcurrido | Hora de inicio y fin con zona, pausas por separado. Usa la misma unidad. | Pendiente | Pendiente |
| Tokens | Suma entrada y salida de todos los turnos cuando el entorno los exponga. Si faltan, aplica a ambos el mismo proxy de caracteres visibles de prompts y respuestas dividido por cuatro. Registra exclusiones de contexto, caché y herramientas y conserva las transcripciones. | Pendiente | Pendiente |
| Intervenciones humanas | Cuenta los envíos iniciados por la persona, incluidos prompt inicial, traspasos, aclaraciones y correcciones. Registra aprobaciones de herramientas y guardado de entregables como acciones separadas. Excluye el evento de aprobación de negocio común a ambas corridas. | Pendiente | Pendiente |
| Pruebas aprobadas | Usa casos aprobados sobre el total esperado de la suite común. Registra fallos, errores, omisiones y no ejecutadas. Reporta aparte las suites propias de los agentes. | Pendiente | Pendiente |
| Cumplimiento | Aplica la lista congelada a cada requisito y su evidencia. Calcula requisitos cumplidos sobre el total aprobado. Registra el motivo de cada incumplimiento o falta de evidencia. | Pendiente | Pendiente |
| MAST | Registra solo incidentes observados que correspondan a una categoría con un fragmento verificable. | Pendiente | Pendiente |

Presenta las diferencias junto con sus artefactos. Una corrida por enfoque describe esas ejecuciones y sus condiciones. Si se repiten las corridas, preserva todos los resultados y documenta el criterio de agregación.
