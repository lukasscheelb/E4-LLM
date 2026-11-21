# Contratos de los cuatro agentes

Los cuatro roles se ejecutan como agentes de Codex: Analista, Planificador, Developer y Reviewer.

| Agente | Herramientas | Entrada | Salida | Término | Skill |
|---|---|---|---|---|---|
| Analista | read, search, edit | Necesidad, fuentes, decisiones | analisis.md | 17 CA contrastados o duda explícita | generar-criterios |
| Planificador | read, search | Análisis y aprobación | plan.md | Cada CA con diseño y prueba | verificar-trazabilidad |
| Developer | read, search, edit, execute | Plan autorizado | src/, tests/, implementacion.md | Código trazable y pruebas reales | pytest-runner |
| Reviewer | read, search | Entrega y evidencia | revision.md por coordinador | Veredicto con evidencia | verificar-trazabilidad |

La escritura y ejecución del Developer permiten implementar y ejecutar pytest; la edición del Analista se limita a análisis. Planificador y Reviewer devuelven texto que guarda el coordinador. La restricción de la ejecución fue por instrucciones, no un sandbox equivalente a tools de VS Code. Las cuatro etapas no se sustituyen por una respuesta general.
