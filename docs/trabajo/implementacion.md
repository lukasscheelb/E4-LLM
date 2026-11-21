# Implementación del evaluador MIRA · multi-r0

**Entorno del rol:** agente de Codex.

**Agente:** Developer, agente separado; perfil seguido por instrucciones, no sesión Copilot/VS Code.
**Estado:** implementación y primera suite local completadas. Pendientes CA-10 con aislamiento OS y veredicto Reviewer.
**Ciclo:** entrega inicial; no se ha recibido rechazo ni iniciado un ciclo de corrección.

## Prerrequisitos y alcance

Se leyó el perfil Developer, el plan completo y su addendum, historia, especificación y respuestas aprobadas, bitácora y las Skills `pytest-runner` y `verificar-trazabilidad`, incluido el script de ejecución y la plantilla matriz.

`git merge-base --is-ancestor cadb048 HEAD` devolvió 0; el diff de los tres documentos aprobados contra `2c625d6` fue vacío. HEAD antes de código fue `5a7b12d`, registro de la autorización humana del plan de `30c7d65` con la respuesta «apruebo, continua». El addendum de catálogo está aceptado en ese registro. No se modificaron esos documentos.

API implementada: `src/mira/evaluador.py::evaluar_caso`, expuesta por `src/mira/__init__.py`. Función determinista con diccionarios; validación estricta, configuración por organización sin respaldo implícito, decisión por prioridad, motivos ordenados y desglose nuevo sin mutación. Las cuatro señales con mínimos son obligatorias; seis numéricas adicionales son opcionales; los tres fraudes requieren booleanos explícitos. No hay cálculo de puntaje, red, almacenamiento, servicios ni Bonsai.

## Archivos de implementación

- `src/mira/__init__.py`, `src/mira/evaluador.py`.
- `tests/conftest.py`, `tests/test_aceptacion.py`, `tests/test_validacion.py`.
- `pyproject.toml`, `requirements-dev.txt` (pytest 9.0.2), `.gitignore` (entorno, caches y temporales).
- README: instrucciones de entorno, ejecución y ejemplo de API.

## Ejecución real

El Python global no tenía pytest. Se creó `.venv`; la primera instalación de pytest falló por sockets bloqueados en sandbox y se repitió con escalación autorizada, finalizando correctamente. Es una incidencia de entorno, no una falla MAST atribuida a un agente.

Comando ejecutado desde la raíz:

```powershell
.\.venv\Scripts\python.exe .github/skills/pytest-runner/scripts/run_pytest.py tests --junitxml docs/evidencia/multi-r0-developer-junit.xml 2>&1 |
    Tee-Object -FilePath docs/evidencia/multi-r0-developer-pytest.log
$LASTEXITCODE
```

**Resultado observado: 173 passed in 0.22s; código de salida 0.** No fallos, errores ni omisiones en esa suite. De esas pruebas, 60 corresponden a variantes de los 16 CA funcionales; 113 amplían validación y addendum. CA-10 no se presenta como una prueba unitaria aprobada: exige evidencia ambiental aún pendiente.

El estado exacto probado está fijado por SHA-256 de código, pruebas, configuración y script en `docs/evidencia/multi-r0-developer-manifest.json`. Son archivos nuevos todavía sin commit durante esta etapa, asociados a HEAD base `5a7b12d`; el manifiesto permite comprobarlos después del commit del coordinador.

Evidencia:

- `docs/evidencia/multi-r0-developer-pytest.log`.
- `docs/evidencia/multi-r0-developer-junit.xml`.
- `docs/evidencia/multi-r0-developer-exit.txt`.
- `docs/evidencia/multi-r0-developer-environment.json` (Python 3.14, Windows y paquetes reales).
- `docs/evidencia/multi-r0-developer-manifest.json`.
- `docs/evidencia/multi-r0-developer.md` (prompt y acciones).

## Matriz requisito → diseño → código → pruebas → resultado

Todos los símbolos de negocio se encuentran en `src/mira/evaluador.py`; las funciones `test_ca*` están en `tests/test_aceptacion.py`. Los conteos proceden del JUnit real anterior.

| Requisito / criterio | Diseño del plan | Código | Prueba y variantes | Resultado |
|---|---|---|---|---|
| RF-01, RF-02 / CA-01 | D-01,D-03 | evaluar_caso | test_ca01_banda_aprobacion: 79,80,84,85,86 | 5 aprobadas |
| RF-02 / CA-02 | D-01,D-02,D-03 | evaluar_caso selección de configuración | test_ca02_aislamiento: X/Y a 87 | 1 aprobada, ambas organizaciones |
| RF-01, RF-02 / CA-03 | D-03 | evaluar_caso bandas | test_ca03_frontera_revision: 59,60,61 | 3 aprobadas |
| RF-03, RF-06 / CA-04 | D-03 | _MINIMOS y evaluar_caso | test_ca04_minimos: inferior/igual/superior por señal | 12 aprobadas |
| RF-01, RF-04, RF-06 / CA-05 | D-01,D-03 | _FRAUDES y evaluar_caso | test_ca05_fraude: 59/85 × activo/inactivo | 4 aprobadas |
| RF-05, RF-06 / CA-06 | D-02,D-03 | evaluar_caso faltantes/desglose | test_ca06_ausencia | 1 aprobada |
| RF-02 a RF-06 / CA-07 | D-03 | evaluar_caso motivos | test_ca07_colision: lista exacta ordenada | 1 aprobada |
| RF-02, RF-07 / CA-08 | D-02 | evaluar_caso configuración, _error | test_ca08_configuracion: ausencia y 5 pares inválidos | 6 aprobadas |
| RF-02, RF-06 / CA-09 | D-01,D-03 | evaluar_caso salida/desglose | test_ca09_resultado: todos los campos requeridos | 1 aprobada |
| RNF-01 / CA-10 | D-04 | implementación sin dependencias de red | Suite mediante skill, aislamiento OS pendiente | No acreditado todavía |
| RF-01, RF-05, RF-07 / CA-11 | D-02 | _entero_en_rango, evaluar_caso, _error | test_ca11_entrada: 7 variantes | 7 aprobadas |
| RF-04, RF-05, RF-07 / CA-12 | D-02 | evaluar_caso indicadores | test_ca12_indicadores: completo y 3 omisiones | 4 aprobadas |
| RF-05, RF-07 / CA-13 | D-02 | evaluar_caso valores | test_ca13_no_aplicable: 4 señales | 4 aprobadas |
| RF-02 / CA-14 | D-01,D-02 | evaluar_caso configuración | test_ca14_sin_expediente | 1 aprobada |
| RF-01, RF-02 / CA-15 | D-03 | evaluar_caso umbrales/bandas | test_ca15_extremos: 0,99,100 con R=0/A=100 | 3 aprobadas |
| RF-02, RF-03, RF-05, RF-06 / CA-16 | D-03 | evaluar_caso alertas y prioridad | test_ca16_colision_sin_fraude: 59/60 | 2 aprobadas |
| RF-03, RF-07 / CA-17 | D-02,D-03 | _entero_en_rango y evaluar_caso | test_ca17_dominio_senal: -1,0,69.5,100,101 | 5 aprobadas |

Recorrido inverso: las pruebas adicionales `test_enteros_estrictos`, estructuras, identificación de configuración y precedencia de errores sustentan RF-01/RF-02/RF-07; fraude y omisión por señal sustentan RF-03/RF-04/RF-05; el orden completo y la no mutación sustentan D-03/RF-06. `test_opcionales_no_alteran_ruta` y `test_opcionales_invalidas` sustentan el addendum aprobado, sin imponer mínimos nuevos. No hay prueba de CA-10 que simule falsamente un entorno aislado.

## Traspaso a Reviewer

Revisar esta entrega, el plan y su aprobación, la revisión documental y la evidencia enlazada. La suite local está en verde; el coordinador debe adjuntar la ejecución aislada cuando la obtenga o conservar CA-10 pendiente. No se emitió autoaprobación, no se inventaron fallas MAST ni rechazo humano. Este rol no creó commits ni modificó la bitácora.

## Addendum posterior · CA-10 acreditado en contenedor sin red

Después de la entrega local anterior, el coordinador ejecutó la suite en un contenedor Linux con aislamiento de red del sistema operativo. Developer leyó el comando, inspección Docker, metadatos de entorno, script de aislamiento, log, JUnit y código de salida conservados. No reejecutó pruebas ni cambió código, tests o manifiesto en este addendum.

- Imagen: `mira-e4-pytest:9.0.2`, ID `sha256:935830869c51ed8e82f269f898b5cc5cf5c70466acd785ab01dc1d362a7c97a4`.
- Entorno real: Python 3.14.10, pytest 9.0.2, Linux/WSL2.
- Comando con `--network none --read-only --tmpfs /tmp:rw,nosuid,nodev,size=64m`; código montado de solo lectura y evidencia montada para escritura.
- Inspección Docker: `HostConfig.NetworkMode=none`, `ReadonlyRootfs=true`, estado terminado con `ExitCode=0`.
- Verificación en proceso antes de pytest: interfaz única `lo`, sin rutas externas; intento TCP a `1.1.1.1:53` rechazado con `OSError [Errno 101] Network is unreachable`.
- El script `docs/evidencia/entorno_aislado.py` invocó el script de la Skill `pytest-runner` sobre `tests`.
- **Resultado real `multi-r0-offline-r1`: 173 passed in 0.27s, retorno 0.** JUnit: 173 pruebas, 0 errores, 0 fallos, 0 omitidas; tiempo de suite 0.268s.
- Se verificó que todos los hashes del manifiesto original de Developer siguen coincidiendo con los archivos probados.

**CA-10 pasa a acreditado por esta evidencia ambiental y de ejecución posterior.** La fila de la matriz anterior documenta el estado histórico de la primera entrega local; esta sección actualiza su resultado sin atribuir aislamiento a esa corrida local. RNF-01 dispone de evidencia de ejecución sin red y sin Bonsai. El veredicto final corresponde a Reviewer.

Evidencia verificable:

- `docs/evidencia/multi-r0-offline-r1-comando.json`
- `docs/evidencia/multi-r0-offline-r1-docker-inspect.json`
- `docs/evidencia/multi-r0-offline-r1-entorno.json`
- `docs/evidencia/multi-r0-offline-r1-pytest.log`
- `docs/evidencia/multi-r0-offline-r1-junit.xml`
- `docs/evidencia/multi-r0-offline-r1-exit.txt`
- `docs/evidencia/offline-image.json`
- `docs/evidencia/entorno_aislado.py`

El primer intento `multi-r0-offline` falló antes de ejecutar pruebas porque el sistema de archivos de solo lectura no tenía directorio temporal utilizable. El coordinador conservó el log y repitió habilitando `/tmp` como tmpfs. Es una corrección real del entorno de prueba, sin cambios en lógica o tests; no se convierte automáticamente en un incidente MAST.
