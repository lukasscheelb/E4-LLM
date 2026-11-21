# Preguntas al representante del cliente

**Estado:** pendientes de respuesta. Para cada pregunta registre la respuesta literal, quién la emitió, fecha, referencia a la evidencia y requisitos afectados. Incorpore las respuestas a la especificación y déjelas vinculadas al registro de aprobación.

## P-01 · Fuentes y corte de aprobación

¿Qué norma y versión gobiernan el componente cuando MIRA v1.4 y MAN-REV v1 indican aprobación desde 80 sin fraude y POL-DEC v2 indica 85 o más como referencia? ¿El corte de 80 es una excepción, un umbral para un proceso concreto o una regla que queda fuera de este caso? Indique la salida de un caso completo, sin fraude y con mínimos satisfechos a 79, 80, 84, 85 y 86. Confirme el rol de la política v1 derogada en E4. Afecta RF-02 y RF-04.

## P-02 · Límites y precisión

¿Los puntajes y umbrales son enteros o admiten decimales? ¿Qué inclusión, redondeo o precisión se aplican en ambos cortes? La expresión «sobre 85» de MIRA v1.4 difiere de «85 o más» en POL-DEC v2, y «60–84» deja valores intermedios si hay decimales. Indique resultados en ambos umbrales y en sus valores vecinos admitidos. Afecta RF-01 y RF-02.

## P-03 · Destinos de revisión y riesgo alto

¿Las salidas son aprobación automática, revisión asistida y escalamiento a supervisor? ¿Se confirma que el rechazo siempre es humano, como establece POL-DEC v2, frente a la expresión «se escala o se rechaza» de MIRA v1.4? ¿Qué destino corresponde a un caso ya bajo el corte de riesgo alto si además presenta fraude, un mínimo incumplido o una señal faltante? Afecta RF-02, RF-04 y RF-06.

## P-04 · Mínimos por señal

¿Se confirman los mínimos 70/75/60/60 para `DOC_AUT`, `BIO_ROSTRO`, `CRUCE_MONTO` y `CRUCE_FECHA` de POL-DEC v2? ¿Varían por organización o proceso? ¿Qué señales son aplicables a cada proceso y qué ocurre con un valor igual a su mínimo? Afecta RF-03.

## P-05 · Fraude, ausencia y colisiones

¿Se confirma que el fraude activo cambia la ruta sin descontar puntaje? ¿Qué diferencia hay entre una señal obligatoria faltante, un indicador inactivo y una señal no aplicable? Proporcione el destino y el motivo esperado para fraude, mínimo incumplido y ausencia, tanto por separado como en combinaciones con puntaje alto y bajo. Afecta RF-03 a RF-06.

## P-06 · Selección de configuración

¿La configuración se elige solo por organización o también por proceso? ¿Cuál rige si existen ambas? ¿Qué debe ocurrir cuando falta la configuración y cuándo pueden aplicarse valores de referencia? ¿Qué valores y restricciones deben cumplir los dos umbrales? Afecta RF-02 y RF-04.

## P-07 · Contrato y datos inválidos

¿El componente recibe el puntaje ya calculado y sus componentes, o debe calcularlo? Si lo calcula, indique fórmula, pesos y tratamiento de señales faltantes. ¿Cómo tratar puntajes ausentes o fuera de rango, tipos inválidos, señales desconocidas y configuraciones incoherentes? Afecta RF-01, RF-02 y RF-05.

## P-08 · Gobernanza de umbrales

MIRA v1.4 menciona al diseñador de flujos y POL-DEC v2 exige dos aprobaciones de supervisor. ¿El componente recibe una configuración ya efectiva o debe validar aprobaciones y vigencia? ¿Quién crea y activa un cambio? Afecta el alcance de RF-02.

## P-09 · Contenido del resultado

¿Qué campos mínimos requiere quien llama al componente? Confirme decisión, motivos, tratamiento de motivos concurrentes, puntaje y desglose, y si debe identificar los valores o la versión de la configuración aplicada. Afecta RF-06.
