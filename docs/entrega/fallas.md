# Fallas observadas e interpretación MAST

La revisión no inventa incidentes ni atribuye decisiones humanas al coordinador. Clasificación analítica basada en [Cemri et al., arXiv 2503.13657v2](https://arxiv.org/html/2503.13657v2), §§4.1 y A.2–A.3. Las etiquetas expresan compatibilidad con la taxonomía, no una anotación certificada.

## F-01 Aporte complementario no incorporado al primer plan

- **Hecho:** la primera salida del Planificador dejó A-02 abierto; un turno posterior leyó la copia CAT-SEN y produjo el addendum.
- **Evidencia:** `docs/evidencia/multi-r0-planificador.md`, sección Resultado conservado y prompt literal del addendum; salida original y addendum en `docs/trabajo/plan.md`.
- **Interpretación:** posible FM-2.5 (consideración insuficiente de otra entrada). No se conoce el momento exacto de entrega del mensaje al agente y no se descarta una carrera de comunicación. No se afirma que haya desobedecido deliberadamente.
- **Debilidad localizada:** `.github/agents/planificador.agent.md`, procedimiento original, pasos 1–3, no exigía un inventario final de aportes complementarios. Es una oportunidad preventiva, no prueba de causa exclusiva.
- **Cambio:** cláusula de inventario y addendum en el perfil. Diff versionado en `docs/evidencia/cierre-prevencion.diff` y en Git.
- **Nueva ejecución:** Planificador aplicó el nuevo inventario en lectura a A-01..05 y CAT-SEN; respuesta conservada en `docs/evidencia/cierre-planificador.md`. No editó el plan ni lo volvió a aprobar.
- **Corrección humana:** Lukas aprobó el addendum, pero el retorno al Planificador fue del coordinador automático. No se cuenta como rechazo humano de una salida.

## F-02 Evaluación de un checkout con el módulo de otro

- **Hecho:** `baseline-comun` importó `mira` del checkout multiagente. La firma `evaluar` no existía allí; 114 fallos y una comprobación ambiental aprobada no eran una medida válida de la línea base.
- **Evidencia:** `docs/evidencia/baseline-comun-pytest.log`, JUnit y comando original. El traceback contiene `AttributeError` en el adaptador. Los logs posteriores `*-comun-r1` muestran 115/115 después de fijar `-c /work/pyproject.toml`.
- **Interpretación:** compatible con FM-3.3 (verificación incorrecta) en la capa de evaluación posterior. No es un fallo de lógica del generalista ni un defecto detectado por Reviewer en el producto.
- **Causa operativa:** descubrimiento automático de configuración pytest en `/audit` antepuso su `src`. La versión original de la suite importaba `mira` sin comprobar su ubicación; conservada byte a byte en `docs/evidencia/historico/aceptacion_comun-v1.py`.
- **Debilidad localizada:** `.github/skills/verificar-trazabilidad/SKILL.md`, paso 3 original contrastaba archivos y resultados, pero no exigía comprobar el módulo realmente cargado. La corrección refuerza la skill; no prueba que aquella omisión haya sido causa única.
- **Cambio:** verificación explícita del origen del módulo, configuración del checkout y guardia `MIRA_SOURCE_ROOT` en la suite común. Véase diff preventivo y Git. El manifiesto original de la suite sigue verificable contra la copia histórica; no se reescribe evidencia anterior.
- **Nueva ejecución real:** `cierre-multi` 115/115 y `cierre-baseline` 115/115, retornos 0, mismo contenedor sin red. La guardia se evalúa en la colección antes de aceptar resultados. No cambió el evaluador.

## Otras incidencias y alcance de la rúbrica

El primer contenedor no tenía un directorio temporal escribible. Se conservó la falla y se añadió tmpfs, sin modificar el producto. También hubo reintento de instalación fuera del sandbox. No se etiquetan automáticamente como MAST.

Estas dos historias aportan observación, interpretación, diff y repetición. La evidencia no demuestra dos fallas MAST con atribución causal concluyente a líneas de agentes/skills ni una corrección humana de salida durante la corrida. El informe declara esa brecha del nivel máximo de la rúbrica. La nueva solicitud de completar la entrega autoriza trabajo, pero no se presenta como un rechazo humano retrospectivo.
