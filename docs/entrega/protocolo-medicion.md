# Protocolo para una futura comparación instrumentada

La evidencia actual no permite completar retrospectivamente tokens, duración total o conteo de permisos. Este protocolo es una mejora reproducible, no una nueva corrida medida ni resultados pendientes rellenados con ceros.

1. Congelar requisitos, suite común, modelo, versiones e imagen antes de los dos desarrollos. Registrar las diferencias inevitables.
2. Usar sesiones nuevas y ramas desde la misma revisión previa al código. Fijar orden o sortearlo antes; impedir lectura de la otra entrega.
3. Registrar inicio al despachar el primer prompt y fin al recibir la entrega revisada. Registrar por separado espera humana, instalación/entorno y tiempo activo. Aplicar el mismo criterio a ambos enfoques.
4. Guardar cada prompt y respuesta completos con IDs y tiempos. Si no hay contadores de tokens, usar para ambos caracteres visibles de prompts/respuestas divididos por cuatro; declarar exclusión del contexto heredado, herramientas, caché y razonamiento no expuesto. No llamarlo consumo real facturado.
5. Contar intervenciones humanas por tipo: encargo, aclaración, corrección, aprobación de negocio, aprobación de herramienta y guardado manual. Los mensajes del coordinador automático quedan separados.
6. Evaluar con la suite común congelada, identidad del código y módulos verificadas, entorno igual y evidencia de aislamiento. Reportar aparte suites propias y cualquier reintento.
7. Conservar todas las repeticiones. Comparar medianas o rangos si hay varias, sin eliminar ejecuciones desfavorables. No inferir superioridad a partir de un solo caso.

Campos mínimos del registro: corrida, enfoque, commit base, modelo/versión, inicio, fin, pausas, número de acciones por tipo, tokens reales o proxy definido, pruebas/criterios/requisitos aprobados, evidencia y límites.
