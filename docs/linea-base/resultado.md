# Línea base: API Python MIRA

Implementación de un generalista en una sesión, sin delegación ni lectura de productos de la corrida multiagente. No se utilizaron perfiles ni skills de roles. Los únicos documentos de negocio consultados fueron los de este worktree. También se leyeron la metodología de línea base y la decisión de coordinación; no se abrieron perfiles/skills enlazados.

## Referencias y autorización

- Rama: `codex/linea-base`; base verificada: `cadb048819b191eac705be26ddae2575986139f9`.
- Revisión documental aprobada: `2c625d6446b6fdba4cdc361c77f71235c4c4b45e`; registro humano transcrito en `docs/bitacora.md` de la base.
- Insumos: historia, especificación y preguntas de `docs/trabajo/`, bitácora y aclaración opcional del prompt literal en [evidencia/prompt.md](evidencia/prompt.md).
- Autorización de proceder de principio a fin incluida en ese prompt. No se inventa una aprobación nueva ni se modificaron documentos aprobados.

## Análisis y diseño

El puntaje es un insumo y permanece intacto. Solo se selecciona configuración por organización; no hay valores predeterminados ni sustitución por otra organización. La ausencia de cuatro numéricas requeridas es condición de negocio. La ausencia de fraude explícito y todo valor fuera del contrato son errores de entrada, sin decisión. La configuración se valida antes del caso. Se devuelven errores estructurados de configuración si no es utilizable.

Plan ejecutado en la misma sesión: (1) leer reglas y aprobación, (2) fijar contrato de función y prioridades, (3) implementar validación y evaluación pura, (4) escribir suite parametrizada por CA y aclaración, (5) ejecutar pytest local preservando evidencia, (6) autoevaluar y registrar límites.

La función `mira.evaluar(organizacion, caso, configuraciones)` acepta diccionarios/Mapping. Configuración por organización: `id` y `version` como cadenas no vacías, `R` y `A` enteros estrictos con 0 <= R < A <= 100. Caso: `puntaje` entero 0..100 y `senales` como mapping. Fraude usa booleanos estrictos: True activo y False inactivo. No se aceptan bool como enteros. Estas representaciones son decisiones técnicas permitidas por la especificación.

Los errores contienen exclusivamente `error: {tipo, campo, codigo}`; el primero se elige de manera documentada en la función. No se emite decisión cuando hay error. Los campos adicionales de caso/configuración se ignoran; los códigos de señal desconocidos son error.

La ruta se decide con prioridad fraude/bajo R, alertas numéricas y banda. Los motivos se ordenan fraude, bajo R, faltantes, mínimos y banda restante; por identificador en cada grupo. El motivo principal es copia del primero. El desglose de ausentes muestra estado y mínimo sin inventar valor/cumplimiento; opcionales presentes muestran solo estado y valor.

## Implementación y reproducción

- [Evaluador](../../src/mira/evaluador.py): validación de configuración/entrada, reglas y desglose.
- [API](../../src/mira/__init__.py): exportación de `evaluar`.
- [Pruebas propias](../../tests/test_evaluador.py): CA parametrizados, opcionales, estructura, orden y ausencia de mutación.
- [Configuración pytest](../../pyproject.toml) y [dependencia](../../requirements-dev.txt).

En PowerShell desde esta raíz:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt
.venv/Scripts/python.exe -m pytest -v --junitxml=resultado.xml
$env:PYTHONPATH = (Resolve-Path src).Path
.venv/Scripts/python.exe -c "from mira import evaluar; print(evaluar('X', {'puntaje':85,'senales':{'DOC_AUT':70,'BIO_ROSTRO':75,'CRUCE_MONTO':60,'CRUCE_FECHA':60,'FRA_EDICION':False,'FRA_MEMORIA':False,'FRA_SINTETICO':False}}, {'X':{'id':'X-1','version':'v1','R':60,'A':85}}))"
```

La API no hace I/O ni depende de pytest en producción. No necesita instalación editable para invocarse con PYTHONPATH apuntando a src. La descarga inicial de pytest puede necesitar red; la suite no consume servicios externos.

## Ejecuciones reales

Sondeo previo: Python 3.14.3 disponible; `python -m pytest --version` informó `No module named pytest`. Se conserva en [00-sondeo.txt](evidencia/00-sondeo.txt). Fue sondeo, no ejecución de suite y no generó JUnit. Se creó `.venv` y se instaló pytest 9.2.0, retorno 0: [log](evidencia/01-instalacion.log), [retorno](evidencia/01-instalacion-retorno.txt). La dependencia fijada coincide con la realmente instalada.

Único intento de suite: `.venv/Scripts/python.exe -m pytest -v --junitxml=docs/linea-base/evidencia/02-pytest.xml`. Resultado **124 passed in 0.20s**, retorno **0**, sin errores, fallos ni skips. [Log completo](evidencia/02-pytest.log), [JUnit](evidencia/02-pytest.xml), [retorno](evidencia/02-pytest-retorno.txt), [versiones](evidencia/versiones.txt). No se modificaron código, pruebas o configuración después de este intento. El [manifiesto SHA256](evidencia/manifiesto-sha256.json) identifica sus cinco archivos y `.gitignore`; las rutas son relativas a la raíz y los hashes corresponden a bytes reales.

## Matriz de aceptación y autoevaluación

Esta es la suite propia del generalista, no una suite común independiente. No se dispone de resultados externos ni de cobertura de líneas/instrumentación. El conteo 124 corresponde a variantes pytest y no a 124 criterios.

| CA | Prueba propia / evidencia | Veredicto |
|---|---|---|
| CA-01 | test_ca01: 79/80/84/85/86 | Cumple |
| CA-02 | test_ca02: organizaciones X/Y y configuración aplicada | Cumple |
| CA-03 | test_ca03: 59/60/61 | Cumple |
| CA-04 | test_ca04: 4 mínimos x 3 fronteras, desglose | Cumple |
| CA-05 | test_ca05: 59/85 x fraude activo/inactivo, puntaje intacto | Cumple |
| CA-06 | test_ca06: falta CRUCE_FECHA, ausencia y banda | Cumple |
| CA-07 | test_ca07: colisión y orden exacto | Cumple |
| CA-08 | test_ca08: configuración ausente y cinco pares inválidos; Y aislada | Cumple |
| CA-09 | test_ca09: explicación, puntaje 90 y configuración | Cumple |
| CA-10 | test_ca10_ejecucion_python_local y ejecución real de suite | Parcial: ejecución local probada; red deshabilitada a nivel OS no acreditada |
| CA-11 | test_ca11_puntaje y test_ca11_senal: siete entradas inválidas | Cumple |
| CA-12 | test_ca12: tres omisiones, aprobación completa | Cumple |
| CA-13 | test_ca13: cuatro no aplicables | Cumple |
| CA-14 | test_ca14: configuración sin expediente aprobatorio | Cumple |
| CA-15 | test_ca15: R=0/A=100 y 0/99/100 | Cumple |
| CA-16 | test_ca16: puntaje 59/60 con falta y mínimo, conservación de motivos | Cumple |
| CA-17 | test_ca17: -1/0/69.5/100/101 | Cumple |

Aclaración posterior: `test_opcionales_aclaracion` cubre las seis señales x ocho valores, con enteros extremos válidos, valores inválidos y bool. `test_orden_lexico_y_omision_opcionales` acredita omisión sin desglose/alerta y orden entre múltiples faltantes/mínimos. `test_no_mutacion_ni_aliases` verifica conservación de entradas y aislamiento de salida.

| Requisito | Diseño / código | Pruebas |
|---|---|---|
| RF-01 | Enteros estrictos, puntaje preservado, sin cálculo | CA-01/03/05/11/15 |
| RF-02 | Selección exacta por organización; validación R/A | CA-01/02/03/08/09/14/15/16 |
| RF-03 | MINIMOS y comparación >= | CA-04/09/13/16/17 |
| RF-04 | FRAUDES explícitos; escalamiento sin descuento | CA-05/07/12 |
| RF-05 | Ausencia distinta de inválido/inactivo | CA-06/07/11/12/13/16 |
| RF-06 | Motivos ordenados, desglose y configuración copiada | CA-04/05/06/07/09/16 |
| RF-07 | _error y validaciones previas a decisión | CA-08/11/12/13/17 y estructura/tipos |
| RNF-01 | API Python pura y pytest sin Bonsai/servicios | Suite local 124/124; aislamiento OS no acreditado |

Autoevaluación: 16/17 CA acreditados completamente por la suite propia y revisión; CA-10 parcial. RF-01..07 cubiertos; RNF-01 cuenta con ejecución local pero falta evidencia OS exigida por CA-10. No se infiere que pasar el test local de CA-10 equivalga a tener red deshabilitada. No se intentó modificar red del host ni se afirmó usar Docker: el prompt informó motor no disponible. Veredicto: entrega funcional con pendiente ambiental explícito; sin aprobación total de los 17 CA.

Limitaciones: no se ha corrido suite común externa, no hay medición de cobertura de líneas ni validación en otro Python. La revisión es autoevaluación del mismo autor, sin revisión independiente. La versión/identificadores de configuración usan cadenas como contrato técnico; campos de gobernanza externos no se verifican.

## Registro de actividad y medición

Inicio real de etapa observado por reloj: **2026-11-21 20:41:36 UTC** (17:41:36 America/Santiago). El inicio del reloj ocurre tras recibir el prompt y efectuar la primera inspección local; no mide latencia anterior. La finalización y duración se registran al cerrar este artefacto en `evidencia/tiempos.json`.

Modelo concreto y contadores de tokens: no disponibles en esta sesión. No se calculó proxy de caracteres porque no existe transcripción íntegra verificable de todos los mensajes/herramientas del agente en archivos; no se inventa métrica. El prompt inicial se conserva íntegro. No hubo mensajes humanos directos adicionales dentro de esta sesión; el origen de autorizaciones/aclaraciones es el prompt del coordinador y la bitácora, sin reconstruir un conteo global de intervenciones humanas.

Incidentes observados: pytest faltaba y se instaló exitosamente. No se clasifican incidentes MAST sin una taxonomía/evidencia suficiente; no se asignan valores ni se afirma ausencia exhaustiva. Se pidieron permisos de herramienta para escrituras concretas fuera de los writable roots iniciales; las llamadas se autorizaron y completaron. Sin commit ni push.
