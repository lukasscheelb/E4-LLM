# Método de aceptación común

La suite `aceptacion_comun.py` fue escrita después de las dos entregas a partir de los 17 criterios de la historia aprobada y el addendum aceptado. Es una evaluación común posterior, no una prueba ciega ni una suite congelada antes de las corridas. No se copió ninguna suite propia de los agentes. Se consultaron la historia y las exportaciones públicas; las firmas y vocabularios de salida fueron suministrados por el coordinador.

La variable `MIRA_ENFOQUE` selecciona un adaptador de firma: `evaluar_caso(caso, configuraciones)` para multi y `evaluar(organizacion, caso, configuraciones)` para baseline. Solo se normalizan mayúsculas de decisión y seis nombres equivalentes de motivos. No se agrega una decisión o motivo faltante, no se cambian rutas, entradas, errores ni desglose. Las diferencias permitidas de representación de una señal ausente no se fuerzan a un esquema único; se comprueba su estado.

Cada enfoque debe ejecutarse en un proceso distinto, con `PYTHONPATH` apuntando solo a su `src`, usando el mismo archivo de prueba y la misma imagen/pytest. CA-10 exige `MIRA_RED_AISLADA=1`, únicamente interfaz loopback, tabla IPv4 sin rutas externas e intento real de conexión que produzca `OSError`. No hay mocks ni monkeypatch de sockets. La evidencia externa del coordinador debe conservar el comando Docker `--network none` y la configuración del contenedor; una variable de entorno por sí sola no acredita aislamiento.

La suite cubre las variantes explícitas de los 16 CA funcionales, una comprobación ambiental CA-10, el addendum opcional y rechazo de bool/float en enteros. Se verifica conservación de argumentos, puntaje y configuración en cada evaluación válida, además de motivos y desglose en los casos de aceptación correspondientes. No equivale a cobertura exhaustiva del espacio de entrada ni a prueba de seguridad.

Esta etapa solo creó la suite y documentó el método. No ejecutó pruebas ni afirma resultados; el coordinador guardará logs, JUnit, versiones, hashes y retornos reales de cada ejecución. Las suites propias tienen tamaños distintos y sus conteos no deben usarse por sí solos como medida de superioridad.
