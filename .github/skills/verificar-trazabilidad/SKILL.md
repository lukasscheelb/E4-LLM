---
name: verificar-trazabilidad
description: Comprueba la correspondencia entre requisitos aprobados, criterios, diseño, código y pruebas mediante referencias localizables.
---

## Procedimiento

1. Fija la revisión de la especificación y la revisión que se evalúa. Aplica la [matriz](references/matriz.md) a cada requisito y criterio.
2. Recorre la matriz en ambos sentidos. Busca requisitos sin cobertura, expectativas de pruebas que difieran de la especificación y conductas agregadas sin requisito aprobado.
3. Contrasta las referencias con los archivos y con la salida efectiva de pytest. Reporta cada brecha con identificador y evidencia de lo encontrado.

## Restricciones

Durante planificación, marca código y ejecución como pendientes. En revisión, una prueba contemplada en un plan carece de evidencia de ejecución hasta contar con su resultado real. Preserva los límites de herramientas del agente que consulta la Skill.
