# Informe MIRA E4

Lukas Scheel (representante de negocio), Francisca Meyer y Sebastian Rodriguez.

## 6.1 Resumen ejecutivo

El sistema llevó una necesidad de MIRA a una API Python implementada, probada y revisada. Cuatro agentes separados realizaron análisis, planificación, desarrollo y revisión. Lukas Scheel aprobó la revisión documental y después el plan. La solución usa el puntaje recibido, aplica umbrales por organización y explica la ruta sin rechazar automáticamente.

La suite propia aprobó 173 pruebas. Una evaluación común posterior aprobó 115 pruebas y los 17 criterios en ambas soluciones, multiagente y generalista. La separación aportó artefactos y revisión independiente, pero esta corrida no demuestra una mejora funcional ni ahorro de costo frente al generalista. Recomendamos medir futuras corridas con el mismo protocolo desde el inicio y verificar la procedencia de cada implementación antes de comparar.

## 6.2 Alternativa elegida y caso

Se eligió la alternativa A porque el problema contiene discrepancias de reglas, configuración y prioridades que requieren aclaración humana antes de programar. El componente académico evalúa puntaje final entero 0–100, cuatro señales con mínimos y tres indicadores de fraude. Las seis señales numéricas opcionales aceptadas se validan y desglosan sin cambiar la ruta.

Equipo: Lukas Scheel (representante de negocio), Francisca Meyer y Sebastian Rodriguez. Herramienta real: Codex Desktop con subagentes; no se ejecutaron perfiles de Copilot. La versión exacta de la aplicación y el identificador del modelo no quedaron expuestos por la sesión. Entorno de pruebas: Windows/Python 3.14.3 y Docker Linux/Python 3.14.10 con pytest 9.0.2. La rotación del representante respecto de E2 queda por confirmar.

## 6.3 Diseño del sistema multiagente

El patrón es secuencial: cada rol consume archivos explícitos de la etapa anterior. El Analista conserva la revisión aprobada y entrega analisis.md. Planificador propone el contrato y las pruebas en plan.md. Developer implementa y entrega evidencia. Reviewer contrasta código, requisitos y resultados sin editar ni ejecutar pruebas.

Se descartó un orquestador especializado porque las dependencias son lineales y las decisiones de negocio siguen siendo humanas. Añadir enrutamiento automático no elimina esas decisiones y aumenta el costo de coordinación. Codex coordinó los despachos y guardó las respuestas; esa función operativa no se presentó como un quinto rol del diseño.

La aprobación documental se refiere a 2c625d6 y está registrada en cadb048, antes del código. El plan de 30c7d65 fue autorizado en 5a7b12d. Los traspasos reales fueron automáticos entre subagentes Codex, a diferencia de los botones manuales previstos inicialmente para VS Code. La diferencia está declarada y no se cuenta como intervención humana.

## 6.3 continuación Roles herramientas y skills

La edición del Analista es necesaria para materializar el análisis; no decide precedencia por el cliente. Developer necesita edición y ejecución para producir la API y pytest. Planificador y Reviewer solo leen y buscan; el coordinador guarda su texto. En esta herramienta esos límites se aplicaron por instrucciones, no mediante los permisos técnicos de los perfiles de VS Code.

generar-criterios encapsula una plantilla reutilizable de condiciones y expectativas. verificar-trazabilidad utiliza una matriz bidireccional de requisito, criterio, diseño, código y prueba. pytest-runner ejecuta pytest con el mismo intérprete y conserva el retorno. Sus recursos se usaron realmente y sus lecturas están registradas. Son procedimientos reutilizables y no sustitutos de los roles.

El diseño mínimo usa evaluar_caso(caso, configuraciones), diccionarios, validación sin coerciones y salida estructurada. Fraude activo o puntaje bajo R escala; después se consideran ausencias y mínimos, y finalmente la banda. Los motivos se conservan en orden estable. El rechazo, cálculo del puntaje y gobernanza de configuraciones quedan fuera de alcance.

## 6.4 Ejecución del caso

La revisión documental y las nueve decisiones más tres aclaraciones precedieron a la corrida. Analista aplicó generar-criterios a los 17 CA y señaló el catálogo incompleto como límite de información. El Planificador aplicó verificar-trazabilidad y produjo el contrato, el diseño y las pruebas previstas.

La primera salida del Planificador no incorporó el contraste complementario de CAT-SEN. El coordinador devolvió ese punto y el Planificador produjo un addendum posterior basado en la copia local de E3. No se atribuyó esa corrección a una persona ni se afirmó identidad con el commit externo no disponible. Lukas aprobó expresamente el plan y las seis opcionales antes de Developer.

Developer verificó la aprobación con Git, conservó los documentos aprobados y escribió la API y las pruebas. Su ejecución real mediante pytest-runner obtuvo 173/173. Los hashes del estado probado y los logs/JUnit identifican los archivos. La normalización CRLF/LF de Git está documentada sin afirmar igualdad de bytes cuando no la hay.

## 6.4 continuación Verificación y control humano

El coordinador inició Docker y preparó una imagen con dependencias antes de aislar la red. Las suites se ejecutaron con network none, fuentes de solo lectura y /tmp en memoria. Solo existía la interfaz lo, no había rutas externas y una conexión TCP real fue rechazada con Errno 101. Así se acreditó CA-10 sin mocks ni desconectar el equipo.

Reviewer inspeccionó implementación, matriz, suites y evidencia de aceptación. Emitió Aprobado en la revisión inicial, sin hallazgos P1/P2 y sin usar ciclos de corrección. Su respuesta se guardó íntegra con normalización de espacios finales. No se inventó un rechazo para utilizar el máximo de dos ciclos.

Las decisiones humanas registradas fueron la aprobación de reglas/revisión documental y la aprobación del plan con su addendum. Las devoluciones del coordinador automático no son correcciones del equipo humano. Falta una evidencia explícita de salida rechazada o corregida por una persona durante la corrida; se declara como brecha de la pauta, no como hecho cumplido.

El generalista trabajó en una sesión sin historial y una rama separada desde cadb048. No recibió los productos multiagente. Su implementación y autoevaluación quedaron en 79c69fd, rama codex/linea-base. La misma evaluación externa se aplicó después a ambas entregas.

## 6.5 Resultados y utilidad

Las suites propias tienen tamaños diferentes. El número de pruebas no permite concluir que una solución tenga más calidad. La suite común posterior utilizó adaptadores de firma y vocabulario, sin cambiar la lógica; ambos enfoques aprobaron 115/115, incluidos los 17 CA. Los siete RF y RNF-01 quedaron cubiertos en esta evaluación.

El tiempo de 258 segundos del generalista mide su sesión, no el experimento entero. Para el multiagente no existe un intervalo completo equivalente: hubo espera humana y preparación compartida. Los contadores de tokens y el total de permisos de herramientas no estuvieron disponibles. No se reconstruyen métricas ficticias a partir de logs parciales.

La suite común se escribió después de desarrollar, no fue ciega ni quedó congelada antes de las corridas. El resultado aporta evidencia de aceptación, pero una sola comparación no permite inferir superioridad estadística. La ventaja observada del multiagente es la separación de responsabilidades y revisión; no se demuestra ahorro de tiempo o tokens.

## 6.6 Análisis de fallas y correcciones

La clasificación se usa como interpretación analítica, no como anotación certificada. MAST distingue fallas de coordinación y de verificación [1]. Conservamos evidencia original, cambio y repetición sin convertir un error de entorno en defecto del evaluador.

F-01: la primera salida del Planificador omitió el aporte complementario de catálogo. Es compatible con FM-2.5, consideración insuficiente de otra entrada, pero no se conoce con certeza cuándo recibió ese mensaje. No puede descartarse una carrera de entrega. La corrección real fue un segundo turno y un addendum, no una decisión inventada del cliente. Se refuerza el perfil con un inventario de aportes y cierre de hallazgos.

F-02: la primera evaluación común del generalista importó el src multiagente por el descubrimiento de configuración de pytest. Produjo 114 fallos de AttributeError que no medían la lógica del generalista. Es compatible con FM-3.3, verificación incorrecta, en la capa de evaluación posterior. Se fijó el archivo de configuración y ambas repeticiones dieron 115/115. Se refuerza la skill para comprobar la ruta del módulo antes de aceptar evidencia.

Las causas operativas y sus límites están en docs/entrega/fallas.md. Los cambios preventivos de perfil/skill no prueban que una línea omitida haya causado por sí sola el incidente. Por ello no afirmamos cumplir el nivel máximo de dos fallas MAST con atribución causal plena. El fallo de temporales del contenedor se conserva como incidencia adicional de entorno.

## 6.7 Discusión

Cuatro roles hicieron visibles las transiciones de análisis, diseño, construcción y revisión. Para este evaluador pequeño, el generalista llegó al mismo resultado funcional con menos etapas. Los cuatro agentes son una decisión pedagógica y de control; la evidencia no acredita que sean la opción de menor costo.

El contexto se preservó mediante archivos, hashes y decisiones explícitas. La información de catálogo mostró el límite de enviar una actualización mientras un agente ya está cerrando su respuesta. Un inventario de aportes pendientes puede reducir omisiones, pero debe comprobarse en corridas futuras.

El control humano fue concreto en dos revisiones, con referencias a commits. La solicitud general de continuar no se usó para aprobar anticipadamente un plan todavía inexistente. Aun así, aprobar un mensaje no demuestra por sí solo la profundidad de la lectura humana; esa calidad de revisión no está medida.

El aislamiento de red, la selección del módulo y la identidad del código probado forman parte del experimento, no solo del producto. Una suite correcta puede producir una comparación inválida si importa otra implementación. Las verificaciones de entorno deben ser anteriores al conteo de resultados.

La ausencia de versión exacta del modelo, consumo completo de tokens y tiempos homogéneos reduce la reproducibilidad experimental. El repositorio permite reproducir reglas y pruebas, pero no reconstruye retrospectivamente todo el costo cognitivo o de coordinación. La siguiente corrida debería medirlo desde el primer despacho y congelar la suite común antes de desarrollar.

## 6.8 Conclusiones

Se completó el recorrido funcional de la alternativa A con reglas aclaradas, aprobación previa, cuatro roles separados, código, pruebas y revisión. El aprendizaje principal es vincular cada decisión con una revisión y cada resultado con el estado que realmente se ejecutó.

La próxima iteración fijaría desde el inicio la herramienta y modelo, una medición simétrica y el inventario de aportes entre agentes. Mantendría los controles humanos y la comparación honesta: en este caso ambas soluciones cumplieron la aceptación, sin evidencia suficiente de ahorro del enfoque multiagente.

## Anexos Referencias y límites de entrega

[1] Cemri et al. Why Do Multi-Agent LLM Systems Fail? arXiv:2503.13657v2, 2025. https://arxiv.org/html/2503.13657v2 (consulta 21-11-2026).

Fuentes del caso y evidencia: repositorio https://github.com/lukasscheelb/E4-LLM; bitácora, plan, revisión y comparación. La lista completa de artefactos, comandos y límites se incluye en docs/entrega/README.md. Las fechas de la pauta discrepan: portada 30/11 y condiciones 23/11/2026 a las 14:00; confirmar con el docente.

Datos no acreditados: rotación del representante respecto de E2, acceso efectivo del docente, versión/modelo de la aplicación, ensayo oral realizado y corrección humana de una salida. El informe los declara para no sustituir verificaciones humanas por afirmaciones del asistente.
