---
name: generar-criterios
description: Convierte requisitos de MIRA en criterios Given/When/Then observables y señala los criterios bloqueados por decisiones pendientes.
---

## Procedimiento

1. Asigna un identificador al requisito y localiza su fuente. Consulta la [plantilla](references/criterio.md) para representar condiciones y expectativas.
2. Formula una precondición controlable, una evaluación y un resultado observable. Para fronteras y reglas que coinciden, escribe filas independientes con identificadores de prueba diferenciables.
3. Clasifica los criterios por estado. Si falta una decisión, documenta la entrada que expone la diferencia y vincula la pregunta `P-xx`.

## Restricciones

Conserva las unidades de la fuente. Usa valores concretos como resultados esperados solo cuando su aplicación esté definida. Mantén un resultado pendiente fuera de los criterios ejecutables hasta resolverlo.
