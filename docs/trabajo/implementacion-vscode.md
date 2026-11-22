# Traspaso de Developer a Reviewer · VS Code

## Revisión y alcance

- Commit probado: `2952d3a8fd35e047300f64c796c3469393fbb331`.
- Aprobación del representante: `cadb048819b191eac705be26ddae2575986139f9`, ancestro de la revisión probada.
- Insumos: [análisis de criterios](analisis-vscode.md), [revisión de trazabilidad](plan-vscode.md) y [plan aprobado](plan.md).
- Developer volvió a ejecutar la suite local de la implementación existente. La comparación con el commit probado deja sin diferencias `src/`, `tests/`, `pyproject.toml` y `requirements-dev.txt`.

## Resultado observado

| Suite local | Aprobadas | Fallos | Errores | Omitidas | Código de salida |
|---|---:|---:|---:|---:|---:|
| `tests/` | 173 | 0 | 0 | 0 | 0 |

La ejecución quedó guardada en el [log de pytest](../evidencia/vscode-developer.log) y en el [reporte JUnit](../evidencia/vscode-developer-junit.xml). Ambos coinciden en el total de 173 casos. Para el criterio CA-10 sigue disponible la [evidencia archivada de la suite común sin red](../evidencia/cierre-multi-entorno.json), [con 115 casos aprobados](../evidencia/cierre-multi-pytest.log).
