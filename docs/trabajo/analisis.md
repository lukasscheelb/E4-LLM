# Análisis de HU-E4-01 · corrida multi-r0

**Agente:** Analista, subagente de Codex que consultó y siguió `.github/agents/analista.agent.md`. No se cargó un perfil de VS Code ni se usó GitHub Copilot. El respeto al rol es por instrucciones, no por un sandbox equivalente al perfil de VS Code.

**Estado:** revisión documental efectuada; no se escribió código ni se ejecutaron pruebas. Los resultados de esta tabla son expectativas aprobadas, no resultados de pytest.

## Insumos y aprobación

- Necesidad del cliente: entrada del caso en el README.
- Historia, especificación y respuestas: revisión `2c625d6446b6fdba4cdc361c77f71235c4c4b45e`.
- Decisión humana: Lukas Scheel; registro independiente `cadb048819b191eac705be26ddae2575986139f9` en `docs/bitacora.md`. La raíz verificó que los documentos aprobados no cambiaron posteriormente. Este agente leyó el registro; no volvió a ejecutar la verificación de Git.
- P-01 a P-09 y P-05.a, P-05.b y P-07.a: respuestas aceptadas en `preguntas-cliente.md`.
- Skill aplicada: `.github/skills/generar-criterios/SKILL.md`, usando el recurso de nivel 3 `references/criterio.md`. Se aplicaron sus campos requisito, fuente, Given, When, Then y estado y su procedimiento de fronteras y colisiones.

Los encabezados históricos de la historia, especificación y respuestas aún dicen que la aprobación está pendiente. El registro posterior y explícito en la bitácora resuelve ese estado; se conservan los archivos de la revisión aprobada sin editarlos.

## Fuentes y límites del contraste

Se inspeccionaron los documentos locales aprobados. La especificación identifica F-01 MIRA v1.4 (§§2.6, 2.7, 2.11 y 2.13), F-02 POL-DEC v2 (§§2–7), F-03 CAT-SEN v3 (§§1 y 6), F-04 MAN-REV v1 (§§1–2), F-05 FAQ-OPE v2, F-06 POL-DEC v1 derogada (§§2–5), F-07 especificación CU-1 y F-08 GUI-INC v2/FIC-PLA en el commit de E3 `dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b`.

La búsqueda por nombres CAT/POL/MIRA dentro de este repositorio no encontró copias del corpus. No se consultaron las URLs remotas ni se verificó el contenido íntegro de E1 o E3 durante esta etapa. El contraste se limita a los extractos y referencias consignados en la especificación y a las decisiones explícitas del representante. Esta limitación no se presenta como una nueva validación del corpus.

## Criterios observables revisados con la plantilla

Estado común de CA-01 a CA-17: aprobado por referencia a la revisión y al registro anteriores; implementación y ejecución pendientes. En cada fila, **When** es una evaluación independiente de cada variante, excepto CA-10, cuyo When es ejecutar la suite local sin red. La base común conserva R=60, A=85, fraude explícitamente inactivo y señales en sus mínimos, salvo variación indicada.

| ID / requisitos | Fuente de decisión | Given / variantes identificables | Then observable |
|---|---|---|---|
| CA-01 / RF-01, RF-02 | P-01, P-02 | CA01-79, -80, -84, -85, -86: puntajes respectivos, caso completo | 79/80/84 revisión; 85/86 aprobación. |
| CA-02 / RF-02 | P-02, P-06, P-09 | CA02-X y -Y: puntaje 87, X A=85, Y A=90, ambas R=60 | X aprueba, Y revisa; cada salida identifica su configuración. |
| CA-03 / RF-01, RF-02 | P-02, P-03 | CA03-59, -60, -61: frontera R | 59 escala; 60 y 61 revisan. |
| CA-04 / RF-03, RF-06 | P-04, P-05, P-09 | CA04-DOC_AUT-69/70/71; BIO_ROSTRO-74/75/76; CRUCE_MONTO-59/60/61; CRUCE_FECHA-59/60/61, una señal por evaluación | Bajo mínimo revisa; igualdad y superior aprueban; motivo y desglose muestran el cumplimiento. |
| CA-05 / RF-01, RF-04, RF-06 | P-02, P-03, P-05, P-09 | CA05-59-activo/inactivo y CA05-85-activo/inactivo, alternando FRA_MEMORIA | Activo escala y encabeza motivos; inactivo con 59 escala por puntaje y con 85 aprueba. Puntaje íntegro. |
| CA-06 / RF-05, RF-06 | P-04, P-05, P-09 | CA06-falta-fecha: 85, sin CRUCE_FECHA | Revisa; ausencia principal y banda conservada. |
| CA-07 / RF-02 a RF-06 | P-03, P-05, P-09 | CA07-colision: 59, FRA_EDICION y FRA_SINTETICO activos, DOC_AUT=69, BIO_ROSTRO omitida | Escala. Orden: FRA_EDICION, FRA_SINTETICO, puntaje bajo R, BIO_ROSTRO ausente, DOC_AUT bajo mínimo. |
| CA-08 / RF-02, RF-07 | P-06, P-07 | CA08-ausente/igual/invertida/R-negativo/A-mayor100/fraccionario: configuración X ausente o (60,60)/(85,60)/(-1,85)/(60,101)/(60.5,85); Y válida | Error estructurado de configuración, sin decisión; no usa Y ni respaldo de referencia. |
| CA-09 / RF-02, RF-06 | P-04, P-05, P-09 | CA09-desglose: 90, DOC_AUT=69, configuración identificada/versionada | Revisa; principal DOC_AUT, banda, puntaje, señales/mínimos y R/A/id/versión presentes. |
| CA-10 / RNF-01 | Encargo E4 | CA10-local: entorno Python con pytest y suite de aceptación disponible | Suite ejecutada sin red y con resultado correcto. Pendiente evidencia real del entorno y ejecución. |
| CA-11 / RF-01, RF-05, RF-07 | P-02, P-07 | CA11-puntaje-ausente/-1/101/80.5/texto85; fraude-desconocido; codigo-NO_CATALOGADA | Cada variante devuelve error estructurado de entrada, sin decisión. |
| CA-12 / RF-04, RF-05, RF-07 | P-05.a | CA12-completo y omision-FRA_EDICION/MEMORIA/SINTETICO, puntaje 85 | Completo aprueba; cada indicador omitido produce error de entrada, sin decisión. |
| CA-13 / RF-05, RF-07 | P-05.b | CA13-no-aplicable-DOC_AUT/BIO_ROSTRO/CRUCE_MONTO/CRUCE_FECHA, una señal por variante | Error estructurado de entrada, sin decisión. |
| CA-14 / RF-02 | P-08 | CA14-sin-expediente: configuración válida, efectiva e identificada, sin aprobaciones adjuntas | Usa configuración, devuelve id/versión y no exige expediente. |
| CA-15 / RF-01, RF-02 | P-02, P-06 | CA15-0/99/100: R=0, A=100, sin alertas | Configuración aceptada; 0/99 revisan, 100 aprueba. |
| CA-16 / RF-02, RF-03, RF-05, RF-06 | P-02, P-03, P-04, P-05, P-09 | CA16-59 y -60: DOC_AUT=69, falta CRUCE_FECHA, sin fraude | 59 escala, principal puntaje; 60 revisa, principal ausencia. Conserva todos los motivos correspondientes. |
| CA-17 / RF-03, RF-07 | P-04, P-05, P-07, P-07.a | CA17-DOC_AUT--1/0/69.5/100/101, puntaje 85 | -1/69.5/101 error de entrada; 0 revisa por mínimo; 100 aprueba. |

## Fronteras y colisiones

- Los cortes de referencia tienen vecinos enteros y valor exacto: 59/60/61 y 84/85/86. Cada mínimo tiene inferior, igualdad y superior en CA-04.
- CA-15 verifica extremos 0/100 y una configuración extrema válida. CA-08 y CA-17 verifican valores fuera de dominio y fraccionarios.
- CA-05 mantiene los mismos puntajes al alternar fraude. CA-07 combina fraude múltiple, riesgo alto, ausencia y mínimo; CA-16 combina ausencia y mínimo al cruzar R sin fraude. Son escenarios distintos que evitan confundir precedencia con una sola alerta.
- Los errores se resuelven antes de emitir una decisión: fraude activo no convierte una entrada inválida en evaluación válida. Una señal numérica omitida es una alerta de negocio; un indicador de fraude omitido es error. Estas diferencias están resueltas expresamente por las aclaraciones, no se requieren nuevas reglas.
- El orden de motivos debe verificarse completo, no solo la ruta o la pertenencia de elementos. La banda baja es el motivo de puntaje bajo R; no se requiere duplicarla como otro motivo de banda.

## Hallazgos y traspaso a Planificador

**No se identificó una contradicción entre las rutas y expectativas explícitas de los 17 criterios que obligue a reabrir P-01 a P-09.** La planificación puede continuar con estas decisiones, manteniendo el control humano sobre el plan antes de implementar.

| ID | Hallazgo | Tratamiento |
|---|---|---|
| A-01 | El contrato técnico no fija nombres de campos Python, representación de activo/inactivo, estructura de error, tipo de organización/id/versión ni tratamiento de errores simultáneos. | Detalles de diseño expresamente delegados al plan. Documentarlos, sin convertir errores en decisiones ni alterar dominios. Evitar coerciones silenciosas; un booleano no debe aceptarse como puntaje entero por herencia de tipos de Python. |
| A-02 | Los documentos nombran cuatro señales numéricas con mínimos y tres indicadores de fraude. También remiten a CAT-SEN v3 sin incorporar el catálogo íntegro; no se conoce aquí si hay más señales numéricas catalogadas que deban aceptarse. | El plan debe declarar exactamente qué códigos admite y señalar su respaldo. No afirmar que todo código distinto de estos siete es desconocido para CAT-SEN v3 sin verificarlo. Si necesita ampliar o restringir el catálogo por una regla de negocio no respaldada, consultar al representante antes de implementar esa conducta. |
| A-03 | La historia exige ejecución con red deshabilitada (CA-10). | Planificar cómo se demostrará el aislamiento de red; ausencia de llamadas de red por inspección no equivale por sí sola a una ejecución con red deshabilitada. |
| A-04 | La documentación aprobada mantiene encabezados de estado anteriores a su aprobación. | Usar siempre el hash aprobado y `cadb048` como referencia. No editar retrospectivamente la revisión aprobada para corregir el encabezado. |
| A-05 | La matriz de negocio está completa, pero no hay diseño, código ni resultados. | Planificador aplica `verificar-trazabilidad`; cada variante anterior debe mapearse a prueba prevista. Código y ejecución siguen pendientes. |

Extensiones de verificación derivadas de RF, sin nuevos requisitos: probar cada indicador activo por separado, omitir cada señal numérica por separado, múltiples ausencias/mínimos ordenados y entradas/configuraciones de tipo inválido; documentar qué criterio o requisito sustenta cada caso. No se exige rechazar automáticamente ni recalcular puntaje, gestionar aprobaciones, acceder a Bonsai o añadir servicios.

**Salida para el traspaso:** este archivo, los tres documentos aprobados, el registro de aprobación y `docs/evidencia/multi-r0-analista.md`. El coordinador conserva el prompt y registra el traspaso real; este agente no aprobó el plan ni autorizó la implementación.
