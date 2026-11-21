# Especificación preliminar · Evaluación de casos MIRA

**Estado: borrador, pendiente de aprobación humana.** Componente académico independiente, Alternativa A del Entregable 4.

## Fuentes inspeccionadas

Los enlaces apuntan al commit `dbc10ac` de E3. La descripción de MIRA v1.4 es un extracto contextual. El corpus docente incluye documentos con estados distintos. La vigencia declarada por el corpus es evidencia para la consulta al cliente y queda pendiente confirmar su aplicación al componente E4.

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

POL-DEC v2 §3 documenta estos mínimos de referencia para E4, pendientes de confirmar con el cliente según [P-04](preguntas-cliente.md).

| Señal | Mínimo consignado |
|---|---:|
| `DOC_AUT` | 70 |
| `BIO_ROSTRO` | 75 |
| `CRUCE_MONTO` | 60 |
| `CRUCE_FECHA` | 60 |

## Caso de uso CU-E4-01

**Actor primario:** sistema que solicita la evaluación para una organización. **Beneficiaria:** persona responsable de la revisión de casos.

**Disparador.** El sistema solicita evaluar un caso mediante su puntaje de confianza, las señales disponibles y la configuración aplicable a su organización.

**Precondición propuesta.** La invocación identifica la organización y suministra los datos de evaluación. El origen del puntaje, la configuración efectiva y la validación de entradas siguen pendientes de confirmación.

**Flujo principal propuesto.**

1. Identificar la configuración aplicable al caso.
2. Evaluar el puntaje, los mínimos, los indicadores de fraude y la disponibilidad de señales según las condiciones aprobadas.
3. Devolver la clasificación y el motivo según el contrato aprobado.

**Flujos alternativos pendientes.** Evaluación en el umbral exacto, configuración ausente o inválida, señal faltante o no aplicable, y concurrencia de condiciones. Los resultados exactos se completan con las respuestas del cliente.

**Postcondición propuesta.** La llamada entrega un resultado explicable. La gestión del caso por una persona, el almacenamiento de evidencias y los módulos de análisis quedan fuera del alcance académico propuesto.

## Requisitos preliminares

| ID | Requisito | Fuentes | Por confirmar |
|---|---|---|---|
| RF-01 | Evaluar un puntaje de confianza en escala de 0 a 100. | F-01, F-02 | P-02, P-07 |
| RF-02 | Clasificar con umbrales de aprobación y revisión efectivos para la organización. | F-01, F-02, F-05, F-08 | P-01, P-02, P-03, P-06, P-07, P-08 |
| RF-03 | Considerar los mínimos individuales al evaluar el caso. | F-01, F-02, F-03 | P-04, P-05 |
| RF-04 | Considerar las señales de fraude activas en la clasificación. | F-01, F-02, F-03, F-04 | P-01, P-03, P-05, P-06 |
| RF-05 | Distinguir señales ausentes de señales inactivas o no aplicables. | F-02, F-03 | P-05, P-07 |
| RF-06 | Entregar una decisión explicable con el motivo que corresponda. | F-01, F-02, F-04, F-05 | P-03, P-05, P-09 |
| RNF-01 | Evaluador independiente en Python, reproducible localmente y verificable con pytest, sin Bonsai ni servicios externos. | Encargo E4 | Alcance académico |

La entrada del puntaje ya calculado y la recepción de una configuración efectiva son propuestas de alcance. Quedan pendientes de confirmación junto con el desglose exigido y la gobernanza de cambios. [Preguntas al representante](preguntas-cliente.md).
