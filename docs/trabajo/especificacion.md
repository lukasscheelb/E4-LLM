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

**Disparador e insumos.** El sistema identifica la organización y proporciona el puntaje final ya calculado y los valores o estados de las señales. La evaluación usa la configuración efectiva de esa organización, identificada por su identificador y versión.

**Flujo principal.** Identificar y validar la configuración de la organización, validar los datos presentes, determinar la banda de puntaje, identificar todas las condiciones concurrentes y devolver la decisión con su explicación.

**Flujos alternativos.** Una de las cuatro señales obligatorias ausente es una condición de negocio. Una entrada inválida o una configuración ausente o incoherente genera un error estructurado sin decisión de negocio.

**Alcance.** El evaluador trabaja en Python de forma local. Quedan fuera del componente el cálculo del puntaje, el análisis de evidencias, el rechazo humano y la gestión de casos. En el procedimiento externo, el diseñador propone cambios a los umbrales y dos supervisores distintos los aprueban. El evaluador valida la estructura y los valores de la configuración efectiva que recibe. Las identidades de los aprobadores y la vigencia corresponden al procedimiento externo.

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

## Resultado de la evaluación

En una evaluación válida se devuelve la decisión, el motivo principal, todos los motivos concurrentes, el puntaje recibido, los valores y estados de las señales con sus mínimos y cumplimiento cuando correspondan, y los dos umbrales aplicados con el identificador y versión de la configuración. El desglose describe la evaluación de las señales. El cálculo del puntaje se realiza fuera del componente.

## Aclaraciones antes de la aprobación

Las nueve decisiones ya constan en el [registro del representante](preguntas-cliente.md). Falta precisar el tratamiento de un indicador de fraude omitido y las exclusiones permitidas bajo el estado no aplicable. CA-12 y CA-13 quedan pendientes hasta incorporar estas precisiones. La aprobación expresa de la revisión documental se registrará en un commit humano independiente.
