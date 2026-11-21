# Preguntas al representante del cliente

**Estado:** respuestas acordadas con el representante e incorporadas a la historia y la especificación. El representante también aceptó las tres aclaraciones de contrato. La aprobación expresa de la revisión documental sigue pendiente.

**Representante del cliente:** Lukas Scheel.
**Fecha:** 21 de noviembre de 2026 (America/Santiago).
**Evidencia:** conversación de trabajo asociada a este repositorio. El representante aceptó la propuesta con «si, hagamos tu propuesta y retorname todas las preguntas con las respuestas seleccionadas» y luego solicitó «actualiza el doc con las preguntas en git y ponele las respuestas que elijimos».
**Procedencia:** las respuestas siguientes transcriben las decisiones propuestas por el asistente y aceptadas por el representante; no son citas literales de respuestas redactadas por este último. Se conservan las preguntas y los requisitos afectados en cada sección.
**Selección:** P-01 A, P-02 A, P-03 A, P-04 A, P-05 B armonizada con P-03, P-06 A, P-07 A, P-08 A y P-09 B.

Este registro no sustituye la aprobación expresa de una revisión concreta de la historia y la especificación ni habilita la implementación. La referencia a esa aprobación se incorporará posteriormente en la bitácora, conforme al flujo del README.

## P-01 · Fuentes y corte de aprobación

¿Qué norma y versión gobiernan el componente cuando MIRA v1.4 y MAN-REV v1 indican aprobación desde 80 sin fraude y POL-DEC v2 indica 85 o más como referencia? ¿El corte de 80 es una excepción, un umbral para un proceso concreto o una regla que queda fuera de este caso? Indique la salida de un caso completo, sin fraude y con mínimos satisfechos a 79, 80, 84, 85 y 86. Confirme el rol de la política v1 derogada en E4. Afecta RF-02 y RF-04.

**Respuesta acordada — opción A:**

Para E4 rige POL-DEC v2. El umbral de aprobación de referencia es 85. Para un caso completo, sin fraude, con mínimos satisfechos y configuración de referencia:

| Puntaje | Resultado |
|---|---|
| 79 | Revisión asistida |
| 80 | Revisión asistida |
| 84 | Revisión asistida |
| 85 | Aprobación automática |
| 86 | Aprobación automática |

El corte de 80 queda fuera de este componente. POL-DEC v1 se conserva únicamente como antecedente histórico y sus reglas derogadas no se aplican.

## P-02 · Límites y precisión

¿Los puntajes y umbrales son enteros o admiten decimales? ¿Qué inclusión, redondeo o precisión se aplican en ambos cortes? La expresión «sobre 85» de MIRA v1.4 difiere de «85 o más» en POL-DEC v2, y «60–84» deja valores intermedios si hay decimales. Indique resultados en ambos umbrales y en sus valores vecinos admitidos. Afecta RF-01 y RF-02.

**Respuesta acordada — opción A:**

Los puntajes y umbrales son enteros entre 0 y 100. No se realiza redondeo: los valores con parte fraccionaria son inválidos.

Sean **R** el umbral inferior de revisión y **A** el umbral de aprobación:

- Puntaje menor que R: escalamiento a supervisor.
- Puntaje mayor o igual que R y menor que A: revisión asistida.
- Puntaje mayor o igual que A: aprobación automática, siempre que no existan alertas.

Con R = 60 y A = 85, sin otras alertas:

| Puntaje | Resultado |
|---|---|
| 59 | Escalamiento a supervisor |
| 60 | Revisión asistida |
| 61 | Revisión asistida |
| 84 | Revisión asistida |
| 85 | Aprobación automática |
| 86 | Aprobación automática |

## P-03 · Destinos de revisión y riesgo alto

¿Las salidas son aprobación automática, revisión asistida y escalamiento a supervisor? ¿Se confirma que el rechazo siempre es humano, como establece POL-DEC v2, frente a la expresión «se escala o se rechaza» de MIRA v1.4? ¿Qué destino corresponde a un caso ya bajo el corte de riesgo alto si además presenta fraude, un mínimo incumplido o una señal faltante? Afecta RF-02, RF-04 y RF-06.

**Respuesta acordada — opción A:**

Las salidas de negocio son aprobación automática, revisión asistida y escalamiento a supervisor. El rechazo siempre es una decisión humana; el componente no rechaza automáticamente.

En una evaluación válida, un puntaje inferior al umbral de revisión siempre provoca escalamiento a supervisor, incluso cuando además existe fraude activo, un mínimo incumplido o una señal numérica obligatoria faltante. El resultado conserva todos los motivos concurrentes.

Los errores de entrada o configuración se informan como errores estructurados, sin emitir una decisión de negocio.

## P-04 · Mínimos por señal

¿Se confirman los mínimos 70/75/60/60 para `DOC_AUT`, `BIO_ROSTRO`, `CRUCE_MONTO` y `CRUCE_FECHA` de POL-DEC v2? ¿Varían por organización o proceso? ¿Qué señales son aplicables a cada proceso y qué ocurre con un valor igual a su mínimo? Afecta RF-03.

**Respuesta acordada — opción A:**

Se confirman los siguientes mínimos fijos para E4:

| Señal | Mínimo |
|---|---:|
| `DOC_AUT` | 70 |
| `BIO_ROSTRO` | 75 |
| `CRUCE_MONTO` | 60 |
| `CRUCE_FECHA` | 60 |

Las cuatro señales son obligatorias y aplicables a todos los procesos incluidos en E4. Los mínimos no varían por organización ni proceso. Un valor igual al mínimo cumple; un valor inferior lo incumple.

## P-05 · Fraude, ausencia y colisiones

¿Se confirma que el fraude activo cambia la ruta sin descontar puntaje? ¿Qué diferencia hay entre una señal obligatoria faltante, un indicador inactivo y una señal no aplicable? Proporcione el destino y el motivo esperado para fraude, mínimo incumplido y ausencia, tanto por separado como en combinaciones con puntaje alto y bajo. Afecta RF-03 a RF-06.

**Respuesta acordada — opción B, armonizada con P-03:**

El fraude activo cambia la ruta sin descontar ni modificar el puntaje.

Se distinguen estos estados:

- **Señal numérica obligatoria faltante:** no se recibió uno de los cuatro datos requeridos por P-04. Su ausencia se considera para elegir la ruta de negocio.
- **Indicador de fraude inactivo:** se recibió explícitamente y no genera una alerta de fraude. Si falta un indicador, se devuelve el error de entrada definido en P-05.a.
- **Estado no aplicable:** queda excluido del contrato según P-05.b.

Para entradas y configuraciones válidas, la clasificación sigue esta prioridad:

1. Fraude activo o puntaje inferior a R: **escalamiento a supervisor**.
2. Sin las condiciones anteriores, señal numérica obligatoria faltante o mínimo incumplido: **revisión asistida**.
3. Sin alertas, puntaje desde R inclusive hasta A exclusive: **revisión asistida**.
4. Sin alertas, puntaje desde A inclusive: **aprobación automática**.

| Condiciones | Resultado | Motivos que se conservan |
|---|---|---|
| Fraude activo, con cualquier puntaje válido | Escalamiento a supervisor | Fraude y demás condiciones detectadas |
| Mínimo incumplido, puntaje ≥ R, sin fraude | Revisión asistida | Mínimo incumplido y banda de puntaje |
| Señal numérica obligatoria faltante, puntaje ≥ R, sin fraude | Revisión asistida | Señal faltante y banda de puntaje |
| Puntaje < R, con mínimos incumplidos o señales faltantes | Escalamiento a supervisor | Riesgo alto y todas las alertas adicionales |
| Fraude, mínimo incumplido y ausencia concurrentes | Escalamiento a supervisor | Todos los motivos detectados |

## P-06 · Selección de configuración

¿La configuración se elige solo por organización o también por proceso? ¿Cuál rige si existen ambas? ¿Qué debe ocurrir cuando falta la configuración y cuándo pueden aplicarse valores de referencia? ¿Qué valores y restricciones deben cumplir los dos umbrales? Afecta RF-02 y RF-04.

**Respuesta acordada — opción A:**

La configuración se selecciona únicamente por organización. E4 no admite configuraciones específicas por proceso.

Cada organización debe tener una configuración explícita. Si falta, el componente devuelve un error estructurado de configuración, sin decisión de negocio. No se aplican valores de referencia automáticamente ni se utiliza la configuración de otra organización.

Los valores 60 y 85 pueden utilizarse al crear explícitamente una configuración. Ambos umbrales deben ser enteros y cumplir:

**0 ≤ R < A ≤ 100.**

## P-07 · Contrato y datos inválidos

¿El componente recibe el puntaje ya calculado y sus componentes, o debe calcularlo? Si lo calcula, indique fórmula, pesos y tratamiento de señales faltantes. ¿Cómo tratar puntajes ausentes o fuera de rango, tipos inválidos, señales desconocidas y configuraciones incoherentes? Afecta RF-01, RF-02 y RF-05.

**Respuesta acordada — opción A:**

El componente recibe el puntaje final ya calculado y los valores o estados de las señales necesarios para evaluar el caso. No calcula ni reconstruye el puntaje, por lo que no requiere fórmula ni pesos.

Las siguientes condiciones producen un error estructurado, sin decisión de negocio:

- Puntaje ausente, fuera del rango 0–100 o con parte fraccionaria.
- Tipos de datos inválidos.
- Valores de señales fuera de su dominio permitido.
- Identificadores de señales desconocidos.
- Configuración ausente o incoherente.

La ausencia de una de las cuatro señales numéricas obligatorias tiene el tratamiento de negocio definido en P-05. Los indicadores de fraude omitidos y los valores numéricos presentes inválidos se tratan conforme a P-05.a y P-07.a.

## P-08 · Gobernanza de umbrales

MIRA v1.4 menciona al diseñador de flujos y POL-DEC v2 exige dos aprobaciones de supervisor. ¿El componente recibe una configuración ya efectiva o debe validar aprobaciones y vigencia? ¿Quién crea y activa un cambio? Afecta el alcance de RF-02.

**Respuesta acordada — opción A:**

El componente recibe una configuración ya aprobada y efectiva.

El diseñador de flujos propone los cambios y dos supervisores distintos los aprueban. La creación, el registro de aprobaciones y la activación se gestionan mediante el procedimiento externo de configuración de la organización y quedan fuera del alcance de E4.

El evaluador valida la estructura y los valores de la configuración recibida, pero no verifica las identidades de los aprobadores, las aprobaciones ni su período de vigencia.

## P-09 · Contenido del resultado

¿Qué campos mínimos requiere quien llama al componente? Confirme decisión, motivos, tratamiento de motivos concurrentes, puntaje y desglose, y si debe identificar los valores o la versión de la configuración aplicada. Afecta RF-06.

**Respuesta acordada — opción B:**

Para una evaluación válida, el resultado incluye:

- Decisión: aprobación automática, revisión asistida o escalamiento a supervisor.
- Motivo principal: la regla que determinó la ruta.
- Todos los motivos concurrentes.
- Puntaje recibido y utilizado, sin modificaciones.
- Desglose de los valores y estados de las señales, sus mínimos y el cumplimiento de estos.
- Umbrales de revisión y aprobación aplicados.
- Identificador y versión de la configuración utilizada.

El desglose corresponde a la evaluación de las señales; no reconstruye el cálculo del puntaje.

Para resolver empates entre motivos, se utiliza un orden estable: **fraude activo, puntaje bajo R, señales obligatorias faltantes, mínimos incumplidos y banda restante de puntaje**. Si hay varios motivos de la misma categoría, se ordenan por identificador de señal.

Cuando una entrada o configuración es inválida, se devuelve el error estructurado correspondiente y no una decisión de negocio.

## Aclaraciones de contrato aceptadas

El representante aceptó expresamente las tres propuestas en el chat de trabajo de E4 con la declaración «Acepto P-05.a, P-05.b y P-07.a tal como están formuladas». La aprobación de la revisión documental se registra por separado.

### P-05.a · Indicador de fraude omitido

`FRA_EDICION`, `FRA_MEMORIA` y `FRA_SINTETICO` deben recibirse explícitamente como activos o inactivos. Si falta cualquiera, se devuelve un error estructurado de entrada sin decisión de negocio. En un caso que cumple los requisitos de aprobación, reemplazar un indicador inactivo por su omisión cambia el resultado de aprobación a error de entrada. Aplica a RF-04, RF-05, RF-07 y CA-12.

### P-05.b · Estado no aplicable

E4 no admite el estado «no aplicable». Declararlo para cualquiera de las cuatro señales numéricas obligatorias devuelve un error estructurado de entrada sin decisión de negocio. La ausencia de una de esas señales sigue la ruta de negocio de P-05. Aplica a RF-05, RF-07 y CA-13.

### P-07.a · Dominio de las señales numéricas

Las señales numéricas solo admiten enteros entre 0 y 100, ambos inclusive. Los valores fraccionarios y fuera de rango devuelven un error estructurado de entrada sin decisión de negocio. Por ejemplo, `DOC_AUT` con valor 69,5 produce un error de entrada. Aplica a RF-03, RF-07 y CA-17.
