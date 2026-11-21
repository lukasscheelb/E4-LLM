---
name: pytest-runner
description: Ejecuta pytest en el entorno Python activo y registra el resultado real y, cuando se solicita, un informe JUnit.
---

## Procedimiento

1. Usa un entorno Python con pytest disponible y abre la raíz de E4. Identifica la revisión o el estado exacto del código que probarás. Conserva un diff si hay cambios sin commit y registra también los archivos nuevos.
2. Ejecuta el [script](scripts/run_pytest.py). Para una corrida completa sobre la futura carpeta `tests/` desde PowerShell, usa el siguiente comando, reemplazando `<id>` por el identificador de la ejecución.

   ```powershell
   python .github/skills/pytest-runner/scripts/run_pytest.py tests --junitxml docs/evidencia/<id>.xml 2>&1 |
       Tee-Object -FilePath 'docs/evidencia/<id>.log'
   $LASTEXITCODE
   ```

3. Registra comando, entorno, ruta de evidencia, código de salida y conteos informados por pytest. Incluye cada reintento con su salida. Distingue fallas, errores, omisiones y ausencia de pruebas según el reporte.

## Restricciones

La suite y su resultado deben corresponder a la revisión registrada. El script usa el mismo intérprete con el que se invoca, sin instalar dependencias. Una corrida sin pruebas, con un error de inicio o con código de salida distinto de cero no acredita una suite aprobada. En la preparación puede consultarse `--help` sin iniciar pytest.
