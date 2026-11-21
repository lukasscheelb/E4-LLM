# Plan técnico de MIRA E4 · multi-r0

**Estado:** propuesta para revisión humana. No autoriza la implementación.
**Rol ejecutado:** Planificador, subagente separado de Codex.
**Revisión documental aprobada:** `2c625d6446b6fdba4cdc361c77f71235c4c4b45e`.
**Registro de aprobación:** `cadb048819b191eac705be26ddae2575986139f9`.
**Insumo de traspaso:** `docs/trabajo/analisis.md`.
**Skill aplicada:** `verificar-trazabilidad`, con `references/matriz.md`, en alcance de diseño. Código, pruebas y resultados siguen pendientes.

## 1. Alcance y condiciones de avance

Implementar un evaluador local y determinista en Python, con una API invocable y pytest. Recibe el puntaje final, las señales y la configuración explícita de la organización. Valida, clasifica y explica; no calcula el puntaje ni modifica configuraciones.

Se conservan los documentos aprobados. Las decisiones nuevas que cambien el comportamiento vuelven al representante.

Antes de Developer deben cumplirse estas condiciones:

1. Verificar nuevamente en Git el registro `cadb048`, su parentesco y la coincidencia de los tres documentos con la revisión aprobada.
2. Resolver la condición de catálogo de la sección 7.
3. La persona revisa este plan y registra qué revisó y si autoriza el paso a Developer.

Los encabezados históricos de los documentos que aún dicen «pendiente de aprobación» no se editan retrospectivamente. Se cita el registro posterior de aprobación.

## 2. Organización prevista

| Archivo | Responsabilidad |
|---|---|
| `src/mira/__init__.py` | Exponer la función pública `evaluar_caso`. |
| `src/mira/evaluador.py` | Constantes de mínimos, validaciones, selección de configuración, decisión, motivos y desglose. |
| `tests/conftest.py` | Datos base y fixtures sin estado compartido mutable. |
| `tests/test_aceptacion.py` | Variantes identificadas de CA-01 a CA-17. |
| `tests/test_validacion.py` | Tipos, estructuras y otras variantes derivadas de RF-01 a RF-07. |
| `pyproject.toml` | Configuración mínima del proyecto y pytest, con importación desde `src/`. |
| `requirements-dev.txt` | Dependencia de pytest con versión utilizada registrada por Developer. |
| `docs/trabajo/implementacion.md` | Resumen, trazabilidad final, revisión probada y evidencia de ejecución. |
| `docs/trabajo/revision.md` | Veredicto de Reviewer, guardado por el coordinador. |
| `docs/evidencia/multi-r0-*` | Prompts, salidas, manifestación del entorno, logs y JUnit reales. |

No se necesita servidor web, base de datos, Bonsai ni servicios remotos. La API Python invocable satisface la interfaz mínima adoptada en el README.

## 3. Diseño D-01 · API y contrato técnico

Firma prevista:

```python
evaluar_caso(caso: dict, configuraciones: dict) -> dict
```

No se realizan coerciones silenciosas. Para puntajes, señales numéricas y umbrales se exige `type(valor) is int`: `True`, `False`, texto, `float` y `None` no son enteros válidos del contrato.

### Entrada

```python
caso = {
    "organizacion": "X",
    "puntaje": 85,
    "senales": {
        "DOC_AUT": 70,
        "BIO_ROSTRO": 75,
        "CRUCE_MONTO": 60,
        "CRUCE_FECHA": 60,
        "FRA_EDICION": False,
        "FRA_MEMORIA": False,
        "FRA_SINTETICO": False,
    },
}

configuraciones = {
    "X": {
        "id": "config-X",
        "version": "1",
        "R": 60,
        "A": 85,
    },
}
```

Decisiones técnicas propuestas:

- Organización, identificador y versión: cadenas no vacías.
- Indicadores de fraude: booleanos estrictos; `True` significa activo y `False`, inactivo.
- Señal numérica ausente: clave omitida. Una clave presente con `None`, texto o cualquier otro valor inválido produce error.
- El texto `"no aplicable"` es inválido.
- Configuraciones: diccionario indexado por organización; solo se consulta la entrada solicitada.
- Los códigos admitidos quedan sujetos a la condición de catálogo de la sección 7.

Estos detalles representan las decisiones de negocio existentes; no introducen nuevos cortes ni rutas.

## 4. Diseño D-02 · Validación y errores

Orden técnico determinista:

1. Validar estructura de `caso`, `configuraciones` e identificador de organización.
2. Localizar y validar exclusivamente la configuración de esa organización.
3. Validar puntaje, diccionario de señales, códigos y valores presentes.
4. Exigir los tres indicadores de fraude.
5. Identificar las señales numéricas omitidas como alertas de negocio, no como errores.

En caso de varios errores, devolver el primero según ese orden; ordenar por identificador los códigos de señales al validarlos. Este desempate es de contrato técnico y no produce una decisión de negocio.

Salida de error:

```python
{
    "ok": False,
    "error": {
        "tipo": "entrada",  # o "configuracion"
        "codigo": "PUNTAJE_INVALIDO",
        "campo": "puntaje",
        "mensaje": "El puntaje debe ser un entero entre 0 y 100.",
    },
}
```

No incluir `decision`, `motivo_principal` ni una clasificación parcial en una salida de error.

Categorías previstas de códigos: estructura inválida, organización inválida, configuración ausente/inválida, puntaje inválido, señal desconocida, valor de señal inválido e indicador omitido. Developer puede concretar nombres sin cambiar las condiciones ni las categorías aprobadas.

## 5. Diseño D-03 · Decisión, motivos y desglose

Para datos válidos:

1. Reunir todos los indicadores activos, ausencias y mínimos incumplidos.
2. Determinar la banda del puntaje.
3. Aplicar la tabla aprobada:
   - Fraude activo o puntaje `< R`: escalamiento.
   - En otro caso, ausencia o mínimo incumplido: revisión.
   - Sin alertas y puntaje `< A`: revisión.
   - Sin alertas y puntaje `≥ A`: aprobación.
4. Ordenar los motivos:
   - `FRAUDE_ACTIVO`, por código de señal.
   - `PUNTAJE_BAJO_R`.
   - `SENAL_FALTANTE`, por código.
   - `MINIMO_INCUMPLIDO`, por código.
   - `PUNTAJE_EN_REVISION` o `PUNTAJE_EN_APROBACION`, cuando la banda no es baja.
5. El primer motivo determina `motivo_principal`. El puntaje bajo R ya representa la banda baja y no se duplica.
6. Construir una salida nueva sin modificar las entradas.

Valores técnicos de decisión:

- `APROBACION_AUTOMATICA`
- `REVISION_ASISTIDA`
- `ESCALAMIENTO_SUPERVISOR`

Forma prevista:

```python
{
    "ok": True,
    "decision": "REVISION_ASISTIDA",
    "motivo_principal": {
        "codigo": "MINIMO_INCUMPLIDO",
        "senal": "DOC_AUT",
    },
    "motivos": [
        {"codigo": "MINIMO_INCUMPLIDO", "senal": "DOC_AUT"},
        {"codigo": "PUNTAJE_EN_APROBACION"},
    ],
    "puntaje": 90,
    "desglose": {
        # Cada señal admitida y su estado.
        # Las cuatro numéricas incluyen valor, mínimo y cumplimiento.
    },
    "configuracion": {
        "id": "config-X",
        "version": "1",
        "R": 60,
        "A": 85,
    },
}
```

En el desglose:

- Señal numérica presente: `estado="presente"`, valor recibido, mínimo y `cumple` booleano.
- Señal numérica omitida: `estado="ausente"`, valor `None`, mínimo y `cumple=None`.
- Indicador de fraude: valor booleano y estado `activo`/`inactivo`.
- Si se admiten otras señales catalogadas, su tratamiento debe concretarse antes de implementar, sin inventar mínimos.

## 6. Diseño D-04 · Pruebas, reproducibilidad y evidencia

Developer implementa pruebas parametrizadas con identificadores visibles `CA01-79`, `CA04-DOC_AUT-69`, etc. Las aserciones verifican rutas, errores, contenido, orden completo de motivos y conservación del puntaje; no solo que la función termine.

El estado base usa R=60, A=85, las cuatro señales exactamente en sus mínimos y los tres indicadores inactivos. Cada variante modifica una condición explícita.

### Matriz de trazabilidad de diseño

En todas las filas, **código pendiente** significa que no se escribió ni inspeccionó una implementación; **ejecución pendiente** significa que no existe todavía resultado de pytest.

| Requisito / criterio | Diseño | Código | Prueba prevista y variantes | Resultado y evidencia |
|---|---|---|---|---|
| RF-01, RF-02 / CA-01 | D-01, D-03 | Pendiente | `test_ca01_banda_aprobacion`: 79/80/84 revisan; 85/86 aprueban. | Pendiente de ejecución |
| RF-02 / CA-02 | D-01, D-02, D-03 | Pendiente | `test_ca02_aislamiento`: puntaje 87; X A=85 aprueba, Y A=90 revisa; configuración propia en cada salida. | Pendiente de ejecución |
| RF-01, RF-02 / CA-03 | D-03 | Pendiente | `test_ca03_frontera_revision`: 59 escala, 60/61 revisan. | Pendiente de ejecución |
| RF-03, RF-06 / CA-04 | D-03 | Pendiente | `test_ca04_minimos`: 12 variantes; DOC_AUT 69/70/71, BIO_ROSTRO 74/75/76, ambos CRUCE 59/60/61. Verificar motivo y desglose. | Pendiente de ejecución |
| RF-01, RF-04, RF-06 / CA-05 | D-01, D-03 | Pendiente | `test_ca05_fraude`: 59/85 × FRA_MEMORIA activo/inactivo; rutas, principal y puntaje íntegro. | Pendiente de ejecución |
| RF-05, RF-06 / CA-06 | D-02, D-03 | Pendiente | `test_ca06_ausencia`: falta CRUCE_FECHA a 85; revisión, ausencia principal y banda conservada. | Pendiente de ejecución |
| RF-02 a RF-06 / CA-07 | D-03 | Pendiente | `test_ca07_colision`: comprobar escalamiento y lista exacta ordenada: dos fraudes, puntaje, ausencia, mínimo. | Pendiente de ejecución |
| RF-02, RF-07 / CA-08 | D-02 | Pendiente | `test_ca08_configuracion`: ausencia, igualdad, inversión, R=-1, A=101, R=60.5. Error sin decisión; no usar Y ni respaldo. | Pendiente de ejecución |
| RF-02, RF-06 / CA-09 | D-01, D-03 | Pendiente | `test_ca09_resultado`: 90 con DOC_AUT=69; verificar todos los campos, ambos motivos y configuración. | Pendiente de ejecución |
| RNF-01 / CA-10 | D-04 | Pendiente | Suite completa con red aislada y prueba de que las conexiones están bloqueadas. Registrar entorno, comando, log y salida real. | Pendiente; método disponible por verificar |
| RF-01, RF-05, RF-07 / CA-11 | D-02 | Pendiente | `test_ca11_entrada`: puntaje ausente/-1/101/80.5/"85"; fraude desconocido; código NO_CATALOGADA. | Pendiente de ejecución |
| RF-04, RF-05, RF-07 / CA-12 | D-02 | Pendiente | `test_ca12_indicadores`: completo aprueba; omisión individual de cada uno de los tres indicadores da error. | Pendiente de ejecución |
| RF-05, RF-07 / CA-13 | D-02 | Pendiente | `test_ca13_no_aplicable`: cuatro señales, una por variante, con estado no aplicable; error sin decisión. | Pendiente de ejecución |
| RF-02 / CA-14 | D-01, D-02 | Pendiente | `test_ca14_sin_expediente`: configuración válida sin aprobaciones adjuntas; se usa y devuelve id/versión. | Pendiente de ejecución |
| RF-01, RF-02 / CA-15 | D-03 | Pendiente | `test_ca15_extremos`: R=0/A=100; 0/99 revisan, 100 aprueba. | Pendiente de ejecución |
| RF-02, RF-03, RF-05, RF-06 / CA-16 | D-03 | Pendiente | `test_ca16_colision_sin_fraude`: 59/60 con ausencia y mínimo; verificar rutas, principal y todos los motivos. | Pendiente de ejecución |
| RF-03, RF-07 / CA-17 | D-02, D-03 | Pendiente | `test_ca17_dominio_senal`: -1/69.5/101 error; 0 revisa; 100 aprueba. | Pendiente de ejecución |

Recorrido inverso de la skill:

- D-01 queda sustentado por RF-01, RF-02, RF-04, RF-06 y los criterios de contrato.
- D-02 cubre RF-05/RF-07 y validaciones de RF-01/RF-02/RF-04.
- D-03 cubre las rutas y explicaciones RF-02 a RF-06.
- D-04 cubre RNF-01 y la evidencia exigida por CA-10.
- Los siete RF y RNF-01 tienen criterios y pruebas previstos.
- Falta completar símbolos de código, node IDs reales y resultados después de la implementación.

Pruebas adicionales derivadas de requisitos: booleanos como puntajes/umbrales/señales, estructuras inválidas, cada fraude activo por separado, cada señal numérica omitida, varias ausencias/mínimos y entradas no modificadas. No se presenta su planificación como ejecución.

### Ejecución de pytest

Tras instalar las dependencias en un entorno local y registrar sus versiones, Developer consulta y aplica `pytest-runner`:

```powershell
python .github/skills/pytest-runner/scripts/run_pytest.py tests --junitxml docs/evidencia/multi-r0-junit.xml 2>&1 |
    Tee-Object -FilePath docs/evidencia/multi-r0-pytest.log
$LASTEXITCODE
```

Antes debe guardar el hash del código probado o una instantánea reproducible con diff y archivos nuevos. Un error de inicio, ausencia de pruebas o salida distinta de cero no acredita pruebas aprobadas.

### Aislamiento de red de CA-10

No deshabilitar adaptadores ni modificar persistentemente la red de la PC del usuario.

Método preferido: ejecutar el entorno Python de pruebas ya preparado en un proceso aislado por el sistema operativo, por ejemplo un contenedor con `--network none`, si el entorno dispone de Docker. Registrar imagen, versiones, comando, estado de aislamiento, intento de conexión rechazado y resultado de la suite mediante el script de la skill. Las dependencias e imagen se preparan antes; no se descargan durante la ejecución aislada.

Developer debe comprobar primero la disponibilidad de ese mecanismo o un equivalente. Si no existe, registrar CA-10 como pendiente y solicitar una alternativa concreta; no afirmar que CA-10 pasó.

Bloquear sockets mediante un fixture o plugin de pytest puede añadirse como comprobación de independencia, pero **no se presentará por sí solo como aislamiento de red del sistema operativo**. Tampoco la inspección del código sustituye esa evidencia.

## 7. Hallazgos resueltos y condición de catálogo

| Hallazgo de Analista | Resolución del plan |
|---|---|
| A-01: contrato técnico abierto | D-01 y D-02 proponen representaciones y errores concretos para revisión humana. |
| A-02: catálogo no íntegro | Condición abierta que debe resolverse antes de implementar una lista cerrada de códigos. |
| A-03: CA-10 sin red | D-04 exige aislamiento de proceso verificable; su disponibilidad sigue pendiente. |
| A-04: encabezados históricos | Se conservan y se usa la aprobación posterior como referencia. |
| A-05: trazabilidad sin implementación | Matriz de diseño aplicada; código, pruebas y ejecución pendientes. |

Los documentos locales identifican siete códigos: cuatro numéricos con mínimos y tres indicadores. Eso no demuestra que CAT-SEN v3 completo contenga solo esos siete.

**Condición para la revisión humana:** respaldar el catálogo íntegro o confirmar expresamente que la API académica E4 admite únicamente esos siete códigos. Si existen otros que deban admitirse, definir antes su inclusión y desglose sin inventar mínimos. La implementación de una lista cerrada queda detenida hasta resolverlo. El resto del diseño y las pruebas de los códigos explícitos puede revisarse desde ahora.

La confirmación de una restricción nueva debe registrarse como decisión del representante; no se atribuirá retroactivamente al documento aprobado.

## 8. Secuencia de ejecución y controles

1. Guardar este plan y su evidencia, conservando la salida original del Planificador.
2. Persona revisa diseño, alcance de catálogo, errores, matriz y estrategia sin red; registra autorización o devolución.
3. Developer verifica el commit de aprobación y el registro del control del plan.
4. Developer implementa D-01 a D-03 y pruebas D-04, conservando cada ejecución real.
5. Developer guarda `implementacion.md` con trazabilidad, estado probado y evidencia.
6. Reviewer consulta el plan, documentos aprobados, cambio y resultados; aplica `verificar-trazabilidad` con solo lectura.
7. Coordinador guarda su veredicto sin corregir su contenido. Si rechaza, se permiten como máximo dos ciclos Developer–Reviewer después de la revisión inicial.
8. Registrar prompts, traspasos, resultados y acciones humanas en la bitácora. Los mensajes del coordinador automático no se cuentan como intervenciones humanas.
9. Conservar para la línea base una rama/sesión separada desde una revisión previa al código. El generalista recibe la especificación aprobada y las decisiones de alcance comunes, pero no el plan ni los productos de esta corrida. Comparar con los mismos criterios y registrar condiciones y diferencias reales.

No se crea una falla o rechazo artificial para satisfacer la rúbrica. Solo se clasifican incidentes MAST realmente observados y respaldados.

## 9. Evidencia de ejecución del Planificador

- Ejecución real: subagente Codex `/root/planificador`; no se cargó el perfil en VS Code. Restricciones de lectura seguidas por instrucciones.
- Se leyó `.github/agents/planificador.agent.md`.
- Se leyeron `verificar-trazabilidad/SKILL.md` y `references/matriz.md`. Su aplicación está materializada en la matriz de 17 criterios y en el recorrido inverso D-01 a D-04.
- Se leyeron análisis, especificación, historia, respuestas y bitácora. La primera lectura agrupada fue truncada; se releyeron la sección de entradas y siguientes de la especificación, la historia y las aclaraciones finales. Las respuestas también constaban en el contexto heredado.
- Herramientas realmente utilizadas: `exec_command` con `Get-Content`/`Select-Object` para lectura, `clock__curr_time` y un mensaje al coordinador mediante `collaboration.send_message`.
- Observación del reloj durante esta etapa: 2026-11-21 20:27:09 UTC, equivalente a 17:27:09 America/Santiago. No es una medición de duración total.
- La verificación Git de la revisión aprobada fue suministrada por el coordinador; este rol no la repitió ni afirmó hacerlo.
- No se escribieron archivos, no se implementó, no se ejecutó pytest ni se creó un commit.
- No se consultó el corpus remoto ni se afirmó conocer exhaustivamente CAT-SEN v3.
- Modelo específico, tokens y duración exacta no expuestos al rol; no se inventan.
- El prompt de despacho íntegro consta en el registro de `collaboration.spawn_agent` del coordinador y debe conservarse junto con esta salida. El coordinador es responsable de guardar la salida y registrar el traspaso.
- **Resultado de la etapa:** plan de diseño entregado, condicionado a resolver catálogo y obtener la revisión humana. No se autoriza Developer.

## Addendum · Contraste posterior de CAT-SEN v3 y CA-10

Después de entregar el plan, Planificador leyó la copia local de CAT-SEN v3 situada en `C:/Users/lukas/Documents/ChatGPT/LLM - E3/LLM_E3/Kit_Entrega_3_MIRA/CU-1_operador_revision/corpus/CAT-SEN_catalogo_senales.md`.

La copia enumera diez señales numéricas: `DOC_AUT`, `DOC_ARIT`, `DOC_LEG`, `DOC_IDIOMA`, `META_FECHA`, `META_DISP`, `BIO_ROSTRO`, `BIO_VIDA`, `CRUCE_MONTO` y `CRUCE_FECHA`; además de los tres indicadores `FRA_EDICION`, `FRA_MEMORIA` y `FRA_SINTETICO`. **No se verificó la identidad de esta copia con el commit `dbc10ac` citado en la especificación**; es evidencia complementaria.

**Propuesta concreta para aprobación del representante junto con el plan:** admitir las seis señales adicionales —`DOC_ARIT`, `DOC_LEG`, `DOC_IDIOMA`, `META_FECHA`, `META_DISP` y `BIO_VIDA`— como opcionales, con enteros de 0 a 100. Cuando estén presentes se validan y aparecen en el desglose, sin mínimo ni indicador de cumplimiento. Su omisión no genera alertas y sus valores no modifican la ruta ni el puntaje. Se mantienen las cuatro señales obligatorias y sus mínimos aprobados. No se incorporan nuevas reglas automáticas a partir de las recomendaciones descriptivas del catálogo.

Esta propuesta **resuelve A-02 únicamente si el representante la acepta expresamente**; no se atribuye retroactivamente a la revisión aprobada.

Respecto de CA-10, el coordinador comprobó que Docker CLI existe, pero el daemon no está disponible. El aislamiento de red y la ejecución de pruebas siguen pendientes; no se presenta el entorno como preparado ni se afirma que CA-10 haya pasado.
