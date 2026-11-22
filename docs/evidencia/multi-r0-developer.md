# Evidencia de Developer · multi-r0

**Identificación del rol:** agente de Codex.

Copia editada de denominaciones y rutas de entorno; véase [la nota de edición](NOTA_EDICION.md). No es una transcripción literal sin cambios.

## Procedencia

Rol real `/root/developer`, agente separado. Perfil seguido por instrucciones; no se afirma carga del perfil en VS Code ni aislamiento técnico por su lista de herramientas. No se delegó ni se creó un commit. No se leyó ningún producto de línea base.

## Prompt íntegro recibido

```text
Ejecuta realmente Developer de .github/agents/developer.agent.md en C:/Users/lukas/Documents/ChatGPT/LLM - E4. Lee perfil, docs/trabajo/plan.md completo incluido addendum, aprobados historia/especificacion/preguntas, Skill pytest-runner y script y verificar-trazabilidad. Verifica Git cadb048 ancestro de HEAD, documentos coinciden con 2c625d6; plan de 30c7d65 autorizado por humano literalmente 'apruebo, continua', registro 5a7b12d en bitacora. Implementa plan sencillo API Python invocable src/mira y tests para 17 CA y robustez. Incluye 10 códigos numéricos catálogo (4 obligatorios con mínimos, 6 opcionales no afectan ruta), tres fraudes booleanos explícitos; estricto enteros no bool, orden motivos exacto, errores sin decisión, no mutar entradas. Sin Bonsai ni red en evaluador. Ejecuta pytest REAL mediante script skill y conserva cada intento/log/JUnit/retorno, manifiesto SHA256 de archivos código/tests/config para estado probado. Actualiza docs/trabajo/implementacion.md con matriz 17 CA→símbolos/pruebas/resultados y evidencia docs/evidencia/multi-r0-developer*. Puedes editar README instrucciones uso/entorno, pyproject, requirements-dev, .gitignore si necesita para caches/env. No editar documentos aprobados ni plan ni bitacora (raíz registra); no Git commit/push ni delegar. No afirmar CA10 aislamiento OS si solo fixtures; raíz está preparando Docker, puedes correr suite local y dejar esa parte pendiente hasta resultado raíz. Docker CLI presente pero daemon no activo actualmente. Limita escritura a este repo no directorios linea-base; NO leer docs/linea-base productos futuros. Escribe prompt íntegro y acciones reales/evidencia, tiempos reloj si disponibles, no inventes duración tokens métricas MAST. Entrega rápida pero completa, pruebas significativas no reflejo trivial de implementación. Sigue perfil por instrucciones (no afirmar sandbox herramientas VSCode). Ejecución el entorno de agentes subagente distinto, NO Copilot. Reporta cualquier bloqueo. Debes devolver resultado real, no plan.
```

## Acciones reales

1. Se leyeron perfil Developer, plan/addendum, especificación, historia, respuestas, bitácora, Skill pytest-runner/script y Skill verificar-trazabilidad/plantilla. La primera lectura agrupada excedió la salida disponible; se releyeron especificación, skills y final del plan/bitácora en una llamada acotada.
2. Se verificó con Git `cadb048` ancestro de HEAD (exit 0), diff de documentos aprobados vacío y autorización del plan registrada en `5a7b12d`.
3. Python global no tenía pytest (`No module named pytest`). Se creó `.venv` en el repo. `pip install pytest==9.0.2` dentro sandbox falló con WinError10013 y terminó en exit 1. Se repitió mediante escalación autorizada, instalando pytest y dependencias; exit 0. No se interpreta como fallo funcional ni MAST.
4. Mediante apply_patch se escribieron API, fixtures, suite de aceptación y validación, pyproject, requirements y .gitignore. Mediante Python se añadieron instrucciones al README y se guardaron la implementación y la evidencia.
5. Antes de pytest se creó manifiesto SHA-256 de código, pruebas, configuración y script con base Git y timestamp; véase `multi-r0-developer-manifest.json`.
6. Se ejecutó realmente el script de la Skill con el intérprete de `.venv`. Se guardaron log, JUnit y código de salida. Hubo una sola ejecución de la suite: **173 aprobadas, 0 fallos/errores/omisiones, 0.22s, retorno 0**. CA-10 no está acreditado por este entorno local.
7. Se extrajeron los conteos del JUnit y se completó la matriz de implementación con los 17 CA (16 funcionales, CA-10 pendiente), 60 variantes de aceptación y 113 pruebas adicionales. Se guardaron versión Python, plataforma, pytest y paquetes mediante comandos reales en `multi-r0-developer-environment.json`.

## Tiempos y límites

- Reloj observado durante primera lectura: 2026-11-21 20:41:09 UTC / 17:41:09 America/Santiago.
- Reloj observado tras pruebas y extracción de evidencia: 2026-11-21 20:45:30 UTC / 17:45:30 America/Santiago.
- Son observaciones de etapa, no medición de duración total de la corrida. La duración 0.22s es la informada por pytest, no el tiempo del agente.
- Modelo específico, tokens y versión exacta de la aplicación no expuestos; no se inventan.
- No se ejecutó aislamiento de red OS ni se modificó la red del usuario. No se clasificaron incidentes MAST ni se fabricaron correcciones para la rúbrica.
- Los mensajes de coordinación y solicitudes de permisos de herramientas no se cuentan aquí como decisiones humanas de negocio; raíz registra intervenciones y aprobación.

## Traspaso

La salida está en `docs/trabajo/implementacion.md`, con referencias reales a pruebas y manifiesto. Reviewer debe revisar en solo lectura; la aprobación final no la emite Developer.

## Comprobación posterior de evidencia sin red

Mensaje literal recibido del coordinador:

```text
Raíz ejecutó suites con Docker --network none --read-only --tmpfs /tmp:rw..., misma imagen mira-e4-pytest:9.0.2 (Python3.14.10 Linux). Resultado multi-r0-offline-r1 173passed 0.27s exit0 y baseline124 exit0. Evidencia real docs/evidencia/multi-r0-offline-r1-{pytest.log,junit.xml,entorno.json,exit.txt,docker-inspect.json,comando.json}, offline-image.json, entorno_aislado.py. Entorno prueba solo interfaz lo, sin rutas y socket 1.1.1.1:53 devuelve Errno101. Primer intento multi-r0-offline y baseline-offline falló antes pytest por FS read-only sin /tmp; preservados logs no cambiar código. Lee evidencia multi y actualiza SOLAMENTE docs/trabajo/implementacion.md con addendum CA10 acreditado aislamiento OS y evidencia posterior raíz, manteniendo resultados locales históricos. No reejecutar suite ni modificar código/tests/manifest. Puedes actualizar docs/evidencia/multi-r0-developer.md con este mensaje literal y comprobación real. Entrega para Reviewer.
```

Developer leyó la evidencia multi citada, el script `entorno_aislado.py`, el final del log del intento fallido y el JUnit exitoso. Una comprobación con SHA-256 confirmó que todos los archivos del manifiesto original siguen coincidiendo. El JUnit informa 173 tests, 0 failures/errors/skipped; log 173 passed in 0.27s y exit.txt 0. Inspección confirma NetworkMode none y tmpfs; metadatos solo lo y Errno101. Se añadió el resultado posterior a `implementacion.md` sin reescribir el estado histórico, sin ejecutar tests ni acceder a productos de línea base. La mención baseline en el mensaje de raíz no se utilizó para evaluar esta implementación.
