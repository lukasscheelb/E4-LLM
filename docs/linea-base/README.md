# Línea base con un solo agente

**Estado:** corrida real completada en `codex/linea-base`, commit `79c69fd`. [Resultados y comparación](comparacion.md). El protocolo siguiente describe el encargo utilizado; no sustituye los resultados medidos.

Corre el mismo caso en un chat nuevo con un solo agente generalista. Usa una rama separada desde la misma revisión previa a la implementación, la misma especificación aprobada y el mismo modelo y entorno cuando estén disponibles. El agente generalista recibe el caso y realiza análisis, plan, implementación y pruebas dentro de su propio chat. Mantén la salida de la corrida multiagente fuera de sus insumos.

> Lee la especificación y la historia aprobadas de MIRA E4 y el registro `cadb048`. Resuelve el mismo caso de principio a fin en este chat. Diseña e implementa una API mínima en Python en `src/`, con pruebas en `tests/` y sin Bonsai. Ejecuta pytest, reporta la cobertura de los criterios aprobados y entrega tu evaluación sin delegar.

Guarda aquí el prompt enviado, la salida, el hash o diff de la implementación y el resultado de pytest. Evalúa ambos enfoques contra los mismos 17 criterios aprobados, con la evidencia de cada corrida. Cuenta el tiempo desde el primer mensaje hasta la entrega revisada de cada corrida, con el mismo criterio.

| Métrica | Qué registrar en cada corrida |
|---|---|
| Tiempo | Inicio, fin y duración en la misma unidad. |
| Tokens | Total real cuando esté disponible. Si falta en alguna corrida, usa para ambas la misma aproximación por caracteres visibles divididos por cuatro y declara sus exclusiones. |
| Intervenciones humanas | Número de acciones de la persona y su tipo. Cuenta los traspasos y correcciones cuando ocurran. |
| Pruebas aprobadas | Aprobadas y total ejecutado, además de fallos, errores y omisiones. Indica qué criterios cubre cada suite. |
| Cumplimiento | Requisitos cumplidos sobre ocho, según los 17 criterios aprobados y su evidencia. |

Presenta los valores reales de ambas corridas y explica diferencias favorables y desfavorables. Registra incidentes MAST solo si ocurrieron y hay evidencia.
