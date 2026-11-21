# Comparación real · multi-r0 frente a un agente generalista

## Entregas comparadas y protocolo

- Multiagente: cuatro subagentes Codex separados (Analista, Planificador, Developer y Reviewer). Los perfiles se siguen por instrucciones; no son perfiles cargados en Copilot/VS Code ni un sandbox por herramientas de rol.
- Generalista: subagente nuevo sin historial (`fork_turns=none`), sin delegación y en worktree/rama aislados desde `cadb048`, anterior a cualquier código. No recibió el plan ni productos multiagente. Solo recibió documentos aprobados y la misma decisión posterior sobre seis señales opcionales.
- Código y autoevaluación originales del generalista: rama `codex/linea-base`, commit [`79c69fd`](https://github.com/lukasscheelb/E4-LLM/tree/79c69fd). [Informe original](https://github.com/lukasscheelb/E4-LLM/blob/79c69fd/docs/linea-base/resultado.md), [evidencia](https://github.com/lukasscheelb/E4-LLM/tree/79c69fd/docs/linea-base/evidencia), [código y pruebas](https://github.com/lukasscheelb/E4-LLM/tree/79c69fd/src).
- Base del código multiagente: `5a7b12d`, posterior a la aprobación expresa del plan. Estado probado identificado por `../evidencia/multi-r0-developer-manifest.json`.
- Verificación real de los 14 hashes de ambas entregas: `../evidencia/verificacion-manifiestos.json`, todos coinciden con los bytes utilizados.
- Las suites propias se ejecutaron primero en Windows. Sus versiones de pytest difieren (9.0.2 multi; 9.2.0 generalista); no se comparan sus duraciones como si fueran el mismo entorno.
- Evaluación posterior común: misma imagen Docker, Python 3.14.10 y pytest 9.0.2, con `--network none`, fuente de solo lectura y temporal en memoria. Docker Desktop fue iniciado por el coordinador; no se desconectó la red del host.
- La suite común fue escrita después de las entregas por otro subagente y se congeló en `../evidencia/evaluacion-manifiesto.json`. No fue una evaluación ciega ni una suite congelada antes de desarrollar; esta limitación debe declararse en el informe.
- Los adaptadores solo normalizan firma y vocabulario de motivos, no corrigen lógica ni resultados. Véase `../evidencia/aceptacion-comun-metodo.md`.

## Resultados observados

| Métrica | Multiagente | Generalista | Interpretación / limitación |
|---|---|---|---|
| Suite propia local | 173/173, 0 fallos/errores/omisiones, 0.22s | 124/124, 0 fallos/errores/omisiones, 0.20s | Suites distintas; mayor conteo no demuestra mayor calidad. |
| Suite propia en entorno aislado común | 173/173, 0.27s | 124/124, 0.31s | Misma imagen y aislamiento, pero suites distintas. |
| Suite común final | 115/115, 0.29s | 115/115, 0.32s | Ambos satisfacen las mismas comprobaciones. Diferencias de centésimas en una sola corrida no permiten inferir rendimiento. |
| Criterios aprobados | 17/17 con suite común, incluida CA-10 OS | 17/17 con suite común, incluida CA-10 OS | Los 16 CA funcionales más evidencia ambiental real. |
| Requisitos | RF-01..07 y RNF-01 cubiertos: 8/8 | RF-01..07 y RNF-01 cubiertos: 8/8 | Cobertura de aceptación en estas ejecuciones, no prueba exhaustiva de corrección. |
| Tiempo total de resolución | No medido íntegramente; observación de Analista 20:24:59 UTC, plan/humano/entorno y revisión posteriores | 258s registrados por su sesión (20:41:36–20:45:54 UTC) | Ventanas distintas: la multi incluye pausa humana y preparación compartida de Docker; baseline excluye evaluación común posterior. No calcular aceleración ni ahorro. |
| Tokens | Contadores no expuestos; proxy completo no reconstruible con evidencia disponible | Contadores no expuestos; proxy completo no reconstruible | No se inventa un total ni se compara un subconjunto desigual como consumo total. |
| Decisiones humanas de negocio de esta corrida | 1 encargo de ejecución y 1 aprobación del plan | 0 mensajes humanos directos en la sesión; hereda el encargo y decisiones comunes por prompt | Alcances distintos, no atribuir costo cero al generalista ni contar coordinación automática como intervención humana. Permisos de herramientas no se contabilizaron globalmente de forma completa. |
| Revisión | Reviewer separado, solo lectura; veredicto en `../trabajo/revision.md` | Autoevaluación del propio autor | Diferencia real de control; no demuestra por sí sola un defecto adicional detectado. |

Las horas son UTC; restar tres horas para America/Santiago en esta fecha. La duración del generalista procede de su archivo `tiempos.json`, no de pytest. Las observaciones del multiagente no se presentan como medición exacta de tiempo total.

## Evidencia de aceptación

Para cada prefijo se conservan `-pytest.log`, `-junit.xml`, `-exit.txt`, `-entorno.json`, `-comando.json` y `-docker-inspect.json` en `docs/evidencia/`:

- `multi-r0-offline-r1`: suite propia multiagente, retorno 0.
- `baseline-offline-r1`: suite propia generalista, retorno 0.
- `multi-r0-comun-r1`: suite común multiagente, retorno 0.
- `baseline-comun-r1`: suite común generalista, retorno 0.

El aislamiento se comprobó en cada proceso: Docker `NetworkMode=none`, únicamente interfaz `lo`, sin rutas externas y conexión TCP a `1.1.1.1:53` rechazada con `Errno 101 Network is unreachable`. No se usan mocks para afirmar CA-10. La imagen y el script están conservados en `offline-image.json`, `Dockerfile.pruebas` y `entorno_aislado.py`.

## Incidencias reales y correcciones del entorno

1. Los intentos `multi-r0-offline` y `baseline-offline` alcanzaron la comprobación de red, pero pytest no pudo iniciar porque `--read-only` dejó al contenedor sin temporales escribibles. Se mantuvo el aislamiento y se añadió `--tmpfs /tmp:rw,nosuid,nodev,size=64m`. Las siguientes ejecuciones `*-offline-r1` pasaron. No se cambió el evaluador.
2. Primer intento común `baseline-comun`: pytest descubrió la configuración de `/audit`, que antepuso el src multiagente a PYTHONPATH. Produjo 114 errores de aserción por `AttributeError` de la API incorrecta y una prueba ambiental aprobada; ese resultado es inválido para medir lógica del generalista. Se fijó `-c /work/pyproject.toml` en PYTEST_ADDOPTS y se repitieron ambos enfoques: 115/115. Se conservaron los intentos originales, sin presentarlos como defectos del generalista.
3. La descarga inicial de pytest del Developer requirió reintento fuera del sandbox. No fue un fallo de negocio.

Son incidencias verificables de coordinación/entorno. No se clasifican como fallas MAST ni se atribuye una causa a líneas de agentes/skills sin evidencia. No se fabricaron dos fallas para completar la rúbrica.

## Lectura de utilidad

En este caso ambos enfoques llegaron al mismo cumplimiento de aceptación. La separación multiagente produjo análisis, diseño, trazabilidad y revisión independiente; el generalista produjo una solución funcional con menos etapas. La evidencia disponible no demuestra una mejora de calidad funcional ni ahorro de tiempo/tokens del multiagente. Para comparar costos con rigor faltan mediciones homogéneas completas y más repeticiones; las diferencias y resultados desfavorables deben conservarse.
