# Historia de usuario HU-E4-01

Como responsable de revisión de una organización, quiero que MIRA evalúe los casos con el puntaje de confianza, las señales y los umbrales aplicables a mi organización, para saber qué casos requieren intervención humana y por qué.

**Estado:** borrador. Los criterios propuestos requieren aprobación. Los criterios que dependen de una resolución del representante conservan la expectativa exacta pendiente.

| Criterio | Requisito | Given | When | Then | Estado |
|---|---|---|---|---|---|
| CA-01 | RF-01, RF-02 | Caso completo, sin fraude y con mínimos satisfechos. Su puntaje es 80, 84 o 85. | Se evalúa cada puntaje con la configuración de referencia confirmada. | Se obtiene la clasificación acordada para cada valor. | Pendiente P-01, P-02 |
| CA-02 | RF-02 | Dos organizaciones con configuraciones válidas confirmadas que sitúan el mismo puntaje en bandas distintas. Las demás entradas coinciden. | Se evalúa el caso para cada organización. | Cada resultado coincide con la clasificación de su propia configuración. | Propuesto. Valores y bandas pendientes de P-02, P-03 y P-06. |
| CA-03 | RF-01, RF-02 | Casos completos en el límite inferior de revisión y en los valores vecinos admitidos. | Se evalúa cada valor. | Cada clasificación sigue la inclusión del límite, la precisión y la salida de riesgo alto aprobadas. | Pendiente P-02, P-03 |
| CA-04 | RF-03 | Un puntaje suficiente para aprobación y una señal aplicable con valor justo inferior, igual o superior al mínimo confirmado. | Se evalúa cada variante sin otras alertas. | El resultado y el motivo reflejan el efecto y la inclusión aprobados del mínimo. | Pendiente P-04 |
| CA-05 | RF-04 | Puntajes en bandas alta y baja, con todo lo demás constante y un indicador de fraude que se alterna entre activo e inactivo. | Se evalúa cada combinación. | La clasificación y el tratamiento del puntaje siguen la regla de fraude y el destino aprobados. | Pendiente P-01, P-03, P-05 |
| CA-06 | RF-05 | Tres casos equivalentes con una señal aplicable ausente, presente inactiva y declarada no aplicable, respectivamente. | Se evalúan los casos. | Cada estado recibe el tratamiento aprobado y la ausencia aparece en el motivo cuando corresponde. | Pendiente P-05, P-07 |
| CA-07 | RF-03, RF-04, RF-05, RF-06 | Un caso con puntaje bajo, fraude activo, una señal bajo mínimo y otra faltante. | Se evalúa una vez. | La ruta y los motivos coinciden con la tabla de colisiones acordada. | Pendiente P-03, P-05, P-09 |
| CA-08 | RF-02 | Una organización sin configuración o con configuración inválida. Otra organización tiene configuración válida. | Se evalúa un caso de la primera organización para cada variante. | La primera recibe el tratamiento acordado para su configuración y conserva el aislamiento entre organizaciones. | Pendiente P-06, P-07 |
| CA-09 | RF-06 | Un caso válido que debe derivarse según una regla confirmada. | Se evalúa el caso. | El resultado identifica la clasificación y la razón que explica la derivación según el contrato acordado. | Propuesto. Detalle pendiente P-09. |
| CA-10 | RNF-01 | Un entorno Python con pytest instalado y los casos aprobados disponibles. | Se ejecuta la suite local con la red deshabilitada. | Se obtienen los resultados esperados para los casos aprobados y la suite concluye correctamente. | Propuesto. Ejecución futura. |
| CA-11 | RF-01, RF-05 | Entradas inválidas individualmente según el contrato, por ejemplo un puntaje fuera de escala o un identificador de señal desconocido. | Se evalúa cada entrada inválida. | Cada entrada recibe el error o tratamiento acordado. | Pendiente P-07 |

[P-08](preguntas-cliente.md) determina si se requiere un criterio adicional para activación y aprobación de cambios de configuración. El cliente puede corregir el alcance durante la revisión del borrador.
