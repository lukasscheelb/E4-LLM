# Especificación para revisión · Evaluación de casos MIRA

**Estado: respuestas incorporadas, pendiente de aprobación humana.** Componente académico independiente, Alternativa A del Entregable 4.

## Fuentes inspeccionadas

Los enlaces apuntan al commit `dbc10ac` de E3. La descripción de MIRA v1.4 es un extracto contextual. El corpus docente incluye documentos con estados distintos. El representante confirmó POL-DEC v2 como base de E4 en P-01 y definió en P-03 y P-05 las rutas específicas de escalamiento para el componente.

| ID | Documento y sección | Hallazgo |
|---|---|---|
| F-01 | [MIRA-DESC v1.4, §§2.6, 2.7, 2.11 y 2.13](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/corpus/descripcion/MIRA_v1.4.md) | Puntaje 0–100 con componentes. Combina el corte de referencia «sobre 85» con aprobación desde 80 sin fraude. Plantea revisar mínimos individuales, ajustar por cliente y proceso, y explicar la derivación. |
| F-02 | [POL-DEC v2, §§2–7](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/Kit_Entrega_3_MIRA/CU-1_operador_revision/corpus/POL-DEC_v2_vigente.md) | Se declara vigente. Referencias 85 o más, 60–84 y menos de 60. Indica supervisión bajo 60, decisión humana de rechazo, mínimos individuales, fraude activo sin descuento, revisión si falta una señal y dos aprobaciones de supervisor para cambios de umbral. |
| F-03 | [CAT-SEN v3, §§1 y 6](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/Kit_Entrega_3_MIRA/CU-1_operador_revision/corpus/CAT-SEN_catalogo_senales.md) | Señales numéricas de 0 a 100. Indicadores de fraude activos o inactivos: `FRA_EDICION`, `FRA_MEMORIA` y `FRA_SINTETICO`. |
| F-04 | [MAN-REV v1, §§1–2](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/Kit_Entrega_3_MIRA/CU-1_operador_revision/corpus/MAN-REV_manual_revision_asistida.md) | Se declara vigente e indica aprobación desde 80 sin fraude. El operador consulta el motivo de derivación. |
| F-05 | [FAQ-OPE v2](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/Kit_Entrega_3_MIRA/CU-1_operador_revision/corpus/FAQ-OPE_preguntas_frecuentes_operadores.md) | El umbral de la organización, los mínimos y las señales de fraude explican derivaciones. Sitúa los cambios de umbral en supervisores. |
| F-06 | [POL-DEC v1, §§2–5](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/Kit_Entrega_3_MIRA/CU-1_operador_revision/corpus/POL-DEC_v1_derogada.md) | Documento histórico derogado. Contenía descuento de 20 puntos por señal de fraude activa, cálculo con información parcial y cambios inmediatos por diseñadores. Sirve para reconocer reglas históricas al contrastar antecedentes. |
| F-07 | [Especificación CU-1 de E3](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/docs/especificacion-cu1.md) | Registra la discrepancia 80/85 y evita elegir precedencia. CU-1 era un asistente para operadores, con un alcance distinto al componente de E4. |
| F-08 | [GUI-INC v2, criterios de aceptación](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/Kit_Entrega_3_MIRA/CU-3_incorporacion_organizaciones/corpus/GUI-INC_v2_vigente.md) y [FIC-PLA](https://github.com/franciscameyer/LLM_E3/blob/dbc10aca40c2da58c7a3dab9d8b8626bc5d1751b/Kit_Entrega_3_MIRA/CU-3_incorporacion_organizaciones/corpus/FIC-PLA_fichas_plantillas.md) | La guía pide dos aprobaciones de supervisor. Las fichas sugieren 85/60 para algunas plantillas y 90/65 para otra. Son propuestas por flujo. |

El representante confirmó los cuatro mínimos fijos y la obligatoriedad de estas señales para E4 en [P-04](preguntas-cliente.md).

| Señal | Mínimo |
|---|---:|
| `DOC_AUT` | 70 |
| `BIO_ROSTRO` | 75 |
| `CRUCE_MONTO` | 60 |
| `CRUCE_FECHA` | 60 |

## Caso de uso CU-E4-01

**Actor primario:** sistema que solicita la evaluación para una organización. **Beneficiaria:** persona responsable de revisar casos.

**Disparador e insumos.** El sistema identifica la organización y proporciona el puntaje final ya calculado y los valores o estados de las señales. La evaluación usa la configuración efectiva de esa organización, con identificador y versión.

**Flujo principal.**

1. Localizar la configuración efectiva de la organización indicada y validar su estructura y sus umbrales.
2. Validar el puntaje y los valores o estados de las señales recibidas. Identificar ausencias de las señales obligatorias.
3. Determinar la banda del puntaje y todas las alertas. Usar la tabla de decisión para elegir la ruta.
4. Construir la salida con la decisión, los motivos ordenados, el desglose y la configuración aplicada.

**Flujos alternativos.** Las rutas de negocio de esta tabla se aplican a entradas y configuraciones válidas.

| Condición | Resultado observable |
|---|---|
| Puntaje desde R y señal obligatoria faltante o bajo su mínimo, con los indicadores de fraude inactivos | Revisión asistida. Se conservan las alertas y la banda de puntaje. |
| Puntaje bajo R con señales obligatorias faltantes o bajo mínimo | Escalamiento a supervisor. Se conservan el motivo de puntaje y las alertas adicionales. |
| Fraude activo con cualquier puntaje válido | Escalamiento a supervisor. El puntaje se conserva y el fraude encabeza el orden de motivos. |
| Entrada inválida o configuración ausente o inválida | Error estructurado según la tabla de errores. La evaluación termina sin emitir una decisión de negocio. |

**Alcance.** El evaluador trabaja en Python de forma local. Quedan fuera del componente el cálculo del puntaje, el análisis de evidencias, el rechazo humano y la gestión de casos. En el procedimiento externo, el diseñador propone cambios a los umbrales y dos supervisores distintos los aprueban. El evaluador valida la estructura y los valores de la configuración efectiva que recibe. Las identidades de los aprobadores y la vigencia corresponden al procedimiento externo.

## Entradas

| Dato | Contrato de negocio | Decisiones |
|---|---|---|
| Organización | Identifica de forma inequívoca a qué organización pertenece la evaluación. La selección de configuración se hace por organización. | P-06 |
| Puntaje final | Obligatorio. Entero de 0 a 100 inclusive y calculado previamente. Se utiliza sin redondeo ni ajuste por fraude. | P-01, P-02, P-05, P-07 |
| Señales numéricas | Se identifican mediante códigos del CAT-SEN v3 y tienen escala de 0 a 100. Los cuatro códigos de la tabla de mínimos siempre aplican. Omitir uno de esos cuatro genera ausencia. Enviar un valor inválido genera un error de entrada. La admisión de fracciones sigue pendiente en P-07.a. | P-04, P-05, P-07, F-03 |
| Indicadores de fraude | `FRA_EDICION`, `FRA_MEMORIA` y `FRA_SINTETICO` tienen dos estados cuando se reciben, activo e inactivo. Omitir un indicador se distingue de declararlo inactivo. La consecuencia de la omisión sigue pendiente en P-05.a. | P-05, P-07, F-03 |
| Configuración efectiva | Una configuración explícita de la organización, con identificador, versión y umbrales enteros R y A. Debe cumplir `0 ≤ R < A ≤ 100`. Los cortes 60 y 85 son de referencia y requieren configuración explícita. | P-02, P-06, P-08, P-09 |

El contrato técnico de Python definirá la representación de estos datos. El procedimiento externo establece que la configuración ya está aprobada y efectiva al entregarla al evaluador.

## Requisitos

| ID | Requisito | Decisiones del representante |
|---|---|---|
| RF-01 | Usar el puntaje final recibido. Los puntajes y umbrales son enteros entre 0 y 100. Los valores fraccionarios son inválidos y el puntaje se conserva en el resultado. | P-02, P-07, P-09 |
| RF-02 | Usar exclusivamente la configuración explícita y efectiva de la organización. Los umbrales cumplen `0 ≤ R < A ≤ 100`. Los valores de referencia 60 y 85 pueden configurarse explícitamente. Aplicar las tres rutas de la tabla de decisión. | P-01, P-02, P-03, P-06, P-08 |
| RF-03 | Evaluar las cuatro señales numéricas obligatorias con los mínimos fijos de la tabla, para todas las organizaciones y procesos de E4. La igualdad con el mínimo cumple. | P-04, P-05 |
| RF-04 | Escalar a supervisor si hay fraude activo, cualquiera sea el puntaje. El fraude conserva el puntaje original. | P-03, P-05 |
| RF-05 | Distinguir una señal obligatoria faltante de un dato inválido, un indicador recibido explícitamente como inactivo y un estado no aplicable autorizado. Las cuatro señales obligatorias siempre aplican. | P-04, P-05, P-07 |
| RF-06 | Entregar una decisión explicable con el motivo principal, todos los motivos concurrentes en orden estable, el puntaje recibido, el desglose de señales y la configuración aplicada. | P-03, P-05, P-09 |
| RF-07 | Informar errores estructurados ante puntaje faltante o inválido, tipos o valores de señal inválidos, identificadores desconocidos y configuración ausente o incoherente. Estos errores carecen de decisión de negocio. | P-03, P-06, P-07, P-09 |
| RNF-01 | Evaluador independiente en Python, reproducible localmente y verificable con pytest, sin Bonsai ni servicios externos. | Encargo E4 |

## Tabla de decisión

En los casos válidos se aplica la primera fila que corresponda. R es el umbral inferior de revisión y A es el de aprobación. El rechazo corresponde a una persona.

| Prioridad | Condición | Decisión |
|---:|---|---|
| 1 | Algún indicador de fraude activo o puntaje < R | Escalamiento a supervisor |
| 2 | Sin la condición anterior y con alguna señal obligatoria faltante o bajo su mínimo | Revisión asistida |
| 3 | Sin alertas y R ≤ puntaje < A | Revisión asistida |
| 4 | Sin alertas y puntaje ≥ A | Aprobación automática |

La presencia simultánea de varias condiciones conserva todos los motivos. El orden confirmado es fraude activo, puntaje bajo R, señal obligatoria faltante, mínimo incumplido y banda restante de puntaje. Dentro de una categoría con varios motivos por señal, se ordena por identificador. El motivo principal corresponde a la regla que determina la ruta, con ese mismo desempate.

## Salidas

| Campo de una evaluación válida | Contenido |
|---|---|
| Decisión | Aprobación automática, revisión asistida o escalamiento a supervisor. |
| Motivo principal y motivos concurrentes | Regla que determina la ruta y lista de las condiciones detectadas, en el orden de P-09. La banda de puntaje se conserva cuando concurre con una alerta. |
| Puntaje | Valor final recibido, conservado íntegramente. |
| Desglose | Valores y estados de las señales. Para las señales con mínimo, incluye el mínimo y el cumplimiento cuando exista un valor evaluable. |
| Configuración aplicada | Umbrales R y A, identificador y versión. |

El rechazo corresponde a una persona. El desglose describe la evaluación de señales y el cálculo del puntaje se realiza antes de invocar el componente.

## Errores

| Condición | Resultado |
|---|---|
| Puntaje ausente, fuera de 0–100, fraccionario o con tipo inválido | Error estructurado de entrada. |
| Señal recibida con código desconocido, tipo inválido o valor fuera de su dominio | Error estructurado de entrada. |
| Configuración de la organización ausente, con estructura inválida o con umbrales que incumplen `0 ≤ R < A ≤ 100` o el tipo entero | Error estructurado de configuración. Se mantiene el aislamiento entre organizaciones. |

En los tres casos la salida contiene el error y carece de decisión de negocio. La ausencia de una de las cuatro señales obligatorias activa el flujo alternativo correspondiente. La estructura concreta del error pertenece al diseño técnico.

## Trazabilidad de aceptación

| Requisito | Criterios | Respuestas aplicables |
|---|---|---|
| RF-01 | CA-01, CA-03, CA-05, CA-11, CA-15 | P-01, P-02, P-05, P-07, P-09 |
| RF-02 | CA-01, CA-02, CA-03, CA-07, CA-08, CA-09, CA-14, CA-15, CA-16 | P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09 |
| RF-03 | CA-04, CA-07, CA-16 | P-04, P-05, P-09 |
| RF-04 | CA-05, CA-07, CA-12 | P-02, P-03, P-05, P-09. P-05.a pendiente. |
| RF-05 | CA-06, CA-07, CA-11, CA-12, CA-13, CA-16 | P-03, P-04, P-05, P-07, P-09. P-05.a y P-05.b pendientes. |
| RF-06 | CA-04, CA-05, CA-06, CA-07, CA-09, CA-16 | P-02, P-03, P-04, P-05, P-09 |
| RF-07 | CA-08, CA-11, CA-13, CA-17 | P-03, P-06, P-07, P-09. P-05.b y P-07.a pendientes. |
| RNF-01 | CA-10 | Encargo E4 |

Los identificadores remiten a la [historia de usuario](historia-usuario.md) y al [registro de respuestas](preguntas-cliente.md). Los criterios de aclaraciones se completan con el resultado esperado cuando el representante responda.

## Aclaraciones antes de la aprobación

Las nueve decisiones ya constan en el [registro del representante](preguntas-cliente.md). Falta precisar el tratamiento de un indicador de fraude omitido (P-05.a), las exclusiones permitidas bajo el estado no aplicable (P-05.b) y si las señales numéricas admiten valores fraccionarios (P-07.a). CA-12 y CA-13 quedan pendientes. CA-17 fija los casos fuera de rango y deja el caso fraccionario sujeto a la aclaración. La aprobación expresa de la revisión documental se registrará en un commit humano independiente.
