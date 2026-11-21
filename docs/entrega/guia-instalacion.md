# Guía para instalar y ejecutar MIRA E4 desde cero

## 1 Requisitos e instalaciones previas

Esta guía permite descargar MIRA E4 en un equipo sin el proyecto y ejecutar la API, la demostración y las pruebas. El recorrido principal usa Windows y PowerShell. La sección 5 incluye macOS y Linux. Se necesita un sistema operativo compatible con las herramientas indicadas y conexión a internet durante la preparación.

La interfaz implementada es una función Python: los resultados se ven en la terminal. No hay una pantalla web ni un servidor que abrir en el navegador. Ejecutar el evaluador y volver a ejecutar los agentes son actividades distintas.

| Herramienta | Cuándo se necesita |
| --- | --- |
| Python 3.10 o superior | Obligatorio para ejecutar. Se propone Python 3.14, usado en las pruebas del proyecto. |
| Git | Para descargar con clone, elegir main o la etiqueta y conservar historial. |
| Visual Studio Code | Editor recomendado para seguir la guía. También puede ejecutarse desde una terminal sin editor. |
| Extensión Python de Microsoft | Para seleccionar el intérprete y trabajar con Python dentro de VS Code. |
| GitHub Copilot y cuenta con acceso | Solo para la sección opcional de agentes. No se necesita para ejecutar la API o pytest. |
| Docker Desktop o Docker Engine | Solo para demostrar aislamiento de red y la suite común. |

### Instalar Python en Windows

Abre [Python para Windows](https://www.python.org/downloads/windows/) e instala el Python Install Manager. Abre una PowerShell nueva y ejecuta los comandos siguientes. Si ya tienes Python compatible, basta con verificar su versión. Fuente: [documentación oficial de Python 3.14](https://docs.python.org/3.14/using/windows.html).

```powershell
py install 3.14
py -3.14 --version
```

Debes ver Python 3.14.x. Instala [Git](https://git-scm.com/install/) y [VS Code](https://code.visualstudio.com/download) usando las opciones apropiadas para tu sistema. Cierra y vuelve a abrir la terminal después de instalar. En Windows, conserva la opción del instalador de Git que permite usarlo desde la línea de comandos.

## 2 Descargar y abrir el proyecto en Windows

### Paso 1 Comprobar las herramientas

Abre PowerShell desde el menú Inicio y escribe los comandos, una línea a la vez. No copies el símbolo de una consola ni el texto de los resultados.

```powershell
git --version
py -3.14 --version
```

Si usas una instalación anterior compatible sin el Install Manager, prueba python --version. Para crear el entorno en el paso siguiente podrás reemplazar py -3.14 por python, comprobando que sea 3.10 o superior.

### Paso 2 Descargar la versión actual de main

Elige una carpeta donde guardar el proyecto. El ejemplo usa Documentos. Si ya existe una carpeta E4-LLM con trabajo propio, utiliza otro nombre para el clon.

```powershell
Set-Location ([Environment]::GetFolderPath("MyDocuments"))
git clone --branch main https://github.com/lukasscheelb/E4-LLM.git
Set-Location E4-LLM
git branch --show-current
Get-ChildItem
```

La rama debe ser main. La raíz contiene README.md, src, tests, scripts, docs, pyproject.toml y requirements-dev.txt. La carpeta .github puede estar oculta. Si GitHub pide autenticación, inicia sesión con una cuenta autorizada; un repositorio privado requiere acceso de su propietario.

### Paso 3 Abrir la carpeta en VS Code

Abre VS Code, elige File > Open Folder / Archivo > Abrir carpeta y selecciona E4-LLM. Abre Terminal > New Terminal / Terminal > Nuevo terminal; selecciona PowerShell. Los comandos siguientes se ejecutan en esa terminal, desde la raíz. Fuente: [configuración de VS Code](https://code.visualstudio.com/docs/setup/setup-overview).

```powershell
Get-Location
Test-Path requirements-dev.txt
```

El segundo comando debe devolver True. En Extensiones busca Python, verifica que el editor sea Microsoft e instálala. No necesitas activar Copilot para esta parte. [Guía oficial de Python en VS Code](https://code.visualstudio.com/docs/python/python-tutorial).

## 3 Preparar Python y ejecutar la demostración

### Paso 4 Crear un entorno del proyecto

Desde E4-LLM, crea .venv e instala las dependencias. Usa el Python que acabas de verificar. El entorno separa las dependencias de este proyecto de las de otros proyectos. [Documentación de venv](https://docs.python.org/3/library/venv.html).

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest --version
```

La última línea debe mostrar pytest 9.0.2. En VS Code pulsa Ctrl+Shift+P, busca Python: Select Interpreter y selecciona .venv. Si no aparece, elige la ruta E4-LLM/.venv/Scripts/python.exe.

Los comandos de esta guía invocan el intérprete por su ruta: no hace falta ejecutar Activate.ps1 ni cambiar las políticas de PowerShell. La descarga de paquetes requiere internet en este paso; después el evaluador funciona localmente.

### Paso 5 Ejecutar los cinco ejemplos

```powershell
.\.venv\Scripts\python.exe scripts/demo.py
```

La terminal imprimirá cinco resultados JSON. El siguiente resumen indica qué debe observarse; cada resultado completo también muestra motivos, señales y configuración.

| Escenario | Resultado esperado |
| --- | --- |
| Puntaje 84, caso completo | REVISION_ASISTIDA |
| Puntaje 85, caso completo | APROBACION_AUTOMATICA |
| Puntaje 59, caso completo | ESCALAMIENTO_SUPERVISOR |
| Fraude activo, mínimo incumplido y ausencia | ESCALAMIENTO_SUPERVISOR con todos los motivos |
| Indicador de fraude omitido | ok: false y error; sin campo decision |

Si aparecen estos resultados, el evaluador está funcionando. El programa termina al imprimirlos; no queda un servicio abierto ni necesita una clave de API.

## 4 Ejecutar las pruebas y volver a usar el proyecto

### Paso 6 Ejecutar pytest mediante la Skill

Ejecuta el script que ya incluye el repositorio. Es un programa Python que inicia pytest con el mismo intérprete; usarlo en terminal no equivale por sí solo a demostrar que un agente cargó la Skill.

```powershell
.\.venv\Scripts\python.exe .github/skills/pytest-runner/scripts/run_pytest.py tests
$LASTEXITCODE
```

En el código de la entrega se esperan 173 passed y retorno 0. La duración depende del computador. Cualquier fallo, error o prueba no ejecutada debe revisarse; no cambies el resultado esperado para ocultarlo.

### Paso 7 Guardar evidencia nueva sin sobrescribir la original

```powershell
New-Item -ItemType Directory -Force tmp | Out-Null
.\.venv\Scripts\python.exe .github/skills/pytest-runner/scripts/run_pytest.py tests `
  --junitxml tmp/mi-junit.xml 2>&1 |
  Tee-Object -FilePath tmp/mi-pytest.log
$LASTEXITCODE
```

Los archivos tmp/mi-pytest.log y tmp/mi-junit.xml corresponden a tu ejecución. Si repites y quieres conservar cada intento, cambia mi por un identificador distinto. La suite local comprueba comportamiento; no acredita por sí sola red deshabilitada. Para CA-10 usa la sección 7.

### Paso 8 Abrirlo otro día

Abre la misma carpeta en VS Code y ejecuta de nuevo demo.py o las pruebas usando .venv. No repitas la instalación mientras el entorno siga disponible y no cambien las dependencias. No copies una .venv desde otro computador: créala de nuevo allí.

### Elegir la versión congelada de la entrega

Para una reproducción académica exacta, crea otro clon con la etiqueta. Esta ruta también tiene demo.py y las 173 pruebas. Conserva el clon de main para consultar la guía actualizada.

```powershell
git clone --branch entrega-3 https://github.com/lukasscheelb/E4-LLM.git E4-LLM-entrega
Set-Location E4-LLM-entrega
git describe --tags --exact-match
```

Debe mostrar entrega-3. Una etiqueta abre un estado detached HEAD: es normal para consultar o ejecutar. Si vas a editarlo, crea antes una rama propia con git switch -c mi-demo; no muevas la etiqueta.

## 5 Comandos equivalentes para macOS y Linux

Se mantienen los mismos archivos y resultados; cambian el instalador y la ruta del intérprete. Estos comandos se escriben en Terminal con bash o zsh, no en PowerShell.

### Instalar herramientas

En macOS instala Python 3.14 desde [python.org](https://www.python.org/downloads/macos/) y Git desde [sus instrucciones oficiales](https://git-scm.com/install/). Instala VS Code para macOS y la extensión Python si usarás editor. Verifica python3 --version y git --version.

En Ubuntu o Debian compatibles, puedes instalar los componentes siguientes. En otras distribuciones usa su gestor de paquetes y los nombres equivalentes. Comprueba que python3 sea 3.10 o superior. [Configuración de Python en Ubuntu](https://ubuntu.com/developers/docs/howto/python-setup/).

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip
python3 --version
git --version
```

### Descargar preparar y ejecutar

```bash
git clone --branch main https://github.com/lukasscheelb/E4-LLM.git
cd E4-LLM
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt
./.venv/bin/python scripts/demo.py
./.venv/bin/python .github/skills/pytest-runner/scripts/run_pytest.py tests
echo $?
```

Espera los cinco ejemplos y 173 passed, con retorno 0. No necesitas activar el entorno. Si tienes varias versiones, usa el ejecutable elegido, por ejemplo python3.14 -m venv .venv, si está instalado.

### Guardar evidencia

```bash
mkdir -p tmp
./.venv/bin/python .github/skills/pytest-runner/scripts/run_pytest.py tests \
  --junitxml tmp/mi-junit.xml > tmp/mi-pytest.log 2>&1
echo $?
cat tmp/mi-pytest.log
```

El primer echo debe mostrar 0; compruébalo inmediatamente después de pytest. En VS Code abre la carpeta y selecciona .venv/bin/python como intérprete. Para otra versión del sistema operativo, usa instaladores compatibles: esta guía no garantiza soporte de equipos o sistemas que ya no admiten Python, Git o VS Code.

## 6 Evaluar un caso propio con la API

La función pública es evaluar_caso(caso, configuraciones). Para probarla sin configurar PYTHONPATH, crea un archivo ejemplo_mira.py directamente en la raíz E4-LLM, al mismo nivel que src y README.md. Pega el código siguiente.

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from mira import evaluar_caso

caso = {
    "organizacion": "X",
    "puntaje": 85,
    "senales": {
        "DOC_AUT": 70, "BIO_ROSTRO": 75,
        "CRUCE_MONTO": 60, "CRUCE_FECHA": 60,
        "FRA_EDICION": False,
        "FRA_MEMORIA": False,
        "FRA_SINTETICO": False,
    },
}
configuraciones = {
    "X": {"id": "X-v1", "version": "1", "R": 60, "A": 85}
}
resultado = evaluar_caso(caso, configuraciones)
print(resultado)
```

Windows: .\.venv\Scripts\python.exe ejemplo_mira.py. macOS/Linux: ./.venv/bin/python ejemplo_mira.py. El resultado debe incluir decision: APROBACION_AUTOMATICA y puntaje: 85.

Usa enteros 0–100 para puntaje y señales numéricas, y True/False para los tres fraudes. No omitas indicadores de fraude. La configuración debe corresponder a la organización y cumplir 0 <= R < A <= 100. Una señal numérica obligatoria omitida genera revisión o escalamiento según la prioridad; un valor inválido genera error sin decisión.

Las cuatro señales con mínimos son DOC_AUT=70, BIO_ROSTRO=75, CRUCE_MONTO=60 y CRUCE_FECHA=60. Las seis numéricas opcionales se describen en el plan; no cambian el puntaje ni la ruta. El evaluador recibe el puntaje calculado previamente.

## 7 Pruebas opcionales con red aislada en Docker

Esta sección sirve para demostrar CA-10 y ejecutar la aceptación común de 115 pruebas. No hace falta Docker para la demo ni para las 173 pruebas locales.

### Preparar Docker

Instala Docker Desktop para [Windows](https://docs.docker.com/desktop/setup/install/windows-install/) o [macOS](https://docs.docker.com/desktop/setup/install/mac-install/). En Linux instala [Docker Engine](https://docs.docker.com/engine/install/) o Desktop compatible. En Windows comprueba los requisitos de WSL 2 y virtualización indicados por Docker. Abre Docker Desktop y espera que su motor esté listo; la existencia de docker.exe no basta.

```powershell
docker version
docker info
docker build -t mira-e4-pytest:9.0.2 -f docs/evidencia/Dockerfile.pruebas docs/evidencia
```

La construcción descarga Python y pytest: hazla con internet antes del aislamiento. El comando siguiente es para PowerShell, desde la raíz. Cada acento grave al final de línea continúa el mismo comando; cópialo sin añadir espacios después del acento. Crea evidencia con un nombre distinto si ya hiciste una ejecución.

```powershell
$ruta = (Get-Location).Path
New-Item -ItemType Directory -Force tmp | Out-Null
docker run --rm --network none --read-only `
  --tmpfs /tmp:rw,nosuid,nodev,size=64m `
  --mount "type=bind,source=$ruta,target=/work,readonly" `
  --mount "type=bind,source=$ruta,target=/audit,readonly" `
  --mount "type=bind,source=$ruta/tmp,target=/evidence" `
  -e PYTHONPATH=/work/src `
  -e "PYTEST_ADDOPTS=-p no:cacheprovider -c /work/pyproject.toml" `
  -e MIRA_ENFOQUE=multi -e MIRA_RED_AISLADA=1 `
  -e MIRA_SOURCE_ROOT=/work/src `
  mira-e4-pytest:9.0.2 `
  python /audit/docs/evidencia/entorno_aislado.py mi-offline `
  /audit/docs/evidencia/aceptacion_comun.py
$LASTEXITCODE
```

Espera 115 passed y retorno 0. En tmp quedan mi-offline-entorno.json, mi-offline-junit.xml y mi-offline-exit.txt. El script exige solo lo, ausencia de rutas externas y una conexión real rechazada. La red del computador permanece conectada. Para ejecutar las 173 pruebas propias, sustituye únicamente el último argumento por tests.

## 8 Volver a ejecutar los agentes en VS Code

Esta parte es opcional y distinta de ejecutar el producto. La corrida guardada se hizo con subagentes separados de Codex. Los archivos del repositorio también describen una ruta para GitHub Copilot en VS Code; no se afirma que esa ruta haya producido la evidencia original.

### Preparar Copilot y una copia de trabajo

Configura GitHub Copilot en VS Code e inicia sesión con una cuenta y acceso al servicio. Disponibilidad, cuotas y modelos dependen del plan. Sigue la [configuración oficial](https://code.visualstudio.com/docs/setup/copilot). No necesitas insertar credenciales en el código de MIRA.

Usa un clon separado para la nueva corrida y una rama propia. Para empezar antes de la implementación, conserva el historial completo y parte del registro de aprobación. No borres los resultados de la entrega.

```powershell
git clone https://github.com/lukasscheelb/E4-LLM.git E4-LLM-corrida
Set-Location E4-LLM-corrida
git switch -c mi-corrida cadb048
code .
```

Si code no se reconoce, abre esa carpeta desde VS Code. Esa revisión contiene perfiles y skills históricos; léelos antes de usarlos. Para repetir con los perfiles mejorados de main, usa otra copia y registra las diferencias: no es la misma configuración experimental.

### Comprobar los perfiles y las skills

Abre el chat con el entorno Copilot. En la paleta de comandos ejecuta Chat: Open Customizations y comprueba los cuatro agentes: analista, planificador, developer y reviewer. Verifica sus archivos de origen .github/agents/. En / busca generar-criterios, verificar-trazabilidad y pytest-runner. Las etiquetas pueden variar con la versión; si no aparecen, consulta la documentación de [agentes](https://code.visualstudio.com/docs/agent-customization/custom-agents) y [skills](https://code.visualstudio.com/docs/agent-customization/agent-skills).

No recrees los perfiles manualmente sin comprobar antes la carpeta abierta y la versión de VS Code. Adjuntar un SKILL.md como contexto es una consulta explícita, no evidencia de carga automática; registra cuál usaste.

### Iniciar Analista

Selecciona analista y envía el encargo: «Lee la necesidad del README, los documentos aprobados y cadb048. Aplica generar-criterios y su plantilla a los 17 criterios. Conserva las decisiones aprobadas y entrega analisis.md con hallazgos y fuentes». Guarda prompt, respuesta, archivos y evidencia del uso real de la skill.

## 9 Traspasos y aprobaciones de una nueva corrida

### Planificador y revisión humana

Selecciona planificador. Entrégale analisis.md y las revisiones aprobadas. Pide aplicar verificar-trazabilidad y devolver el plan técnico con API, tareas y pruebas por criterio. Guarda su salida como docs/trabajo/plan.md, sin atribuir al agente una escritura que realizó la persona.

Antes de Developer, el representante debe revisar y autorizar el plan concreto de la nueva corrida. La aprobación histórica de otro plan no aprueba cambios nuevos. Registra la revisión, la declaración real y la decisión en la bitácora; no completes ese registro por anticipado.

### Cómo registrar una aprobación real

Si la revisión documental cambia, guarda primero los documentos en un commit, recibe aprobación expresa de ese hash y crea otro commit dedicado únicamente a docs/bitacora.md. Para el plan registra también su revisión y autorización. Configura tu identidad Git con tus datos reales si Git no la conoce.

```powershell
git add -- docs/bitacora.md
git diff --cached --name-only
git diff --cached -- docs/bitacora.md
```

Continúa solo si el listado contiene únicamente la bitácora y la declaración corresponde a una aprobación real. Entonces ejecuta git commit -m "docs: registrar aprobación humana". No añadas una plantilla vacía como si fuera aprobación.

### Developer y Reviewer

Selecciona developer, entrega plan y aprobación y pide verificar el parentesco Git, implementar y ejecutar pytest con pytest-runner. Conserva cada log/JUnit, retorno y hash del estado probado. Usa un entorno Python preparado dentro de ese clon.

Después selecciona reviewer, con solo lectura y búsqueda. Entrega implementación, plan, requisitos y evidencia. Guarda su veredicto como docs/trabajo/revision.md. Si rechaza, pasa los hallazgos a Developer y registra el número de ciclo: máximo dos correcciones después de la revisión inicial.

Si los botones de traspaso no están disponibles, selecciona cada agente manualmente y adjunta el archivo de la etapa anterior. No reemplaces cuatro roles por una sola respuesta general. Una nueva respuesta de agentes puede diferir de la anterior: mide y registra lo que ocurrió, sin copiar resultados históricos como si fueran nuevos.

## 10 Problemas frecuentes y comprobación final

| Problema | Qué revisar |
| --- | --- |
| python o py no se reconoce | Instala Python, abre otra terminal y verifica la versión. Si funciona python pero no py, usa python para crear .venv. |
| git no se reconoce | Instala Git con acceso desde terminal y abre una nueva. |
| code no se reconoce | Abre VS Code desde su icono y usa Archivo > Abrir carpeta. |
| No se encuentra requirements-dev.txt | La terminal no está en la raíz E4-LLM. Comprueba Get-Location y Get-ChildItem. |
| No module named pytest | Instala requirements-dev.txt usando el mismo .venv que ejecutará las pruebas. |
| No module named mira | Ejecuta scripts/demo.py o el ejemplo de la sección 6. Una sesión Python suelta no agrega src automáticamente. |
| PowerShell bloquea Activate.ps1 | No necesitas activarlo: usa .venv/Scripts/python.exe directamente. |
| pip no descarga paquetes | Revisa conexión, proxy o restricciones del equipo. No confundir descarga con fallo de lógica. |
| Docker no conecta al motor | Abre Docker Desktop y comprueba docker info. Revisa requisitos del backend según documentación. |
| Pruebas en otra implementación | En la suite común fija -c al checkout y MIRA_SOURCE_ROOT a su src; conserva el intento inválido. |
| GitHub dice Repository not found | Comprueba URL y acceso de la cuenta. Solicita permiso al propietario si es privado. |

### Lista final

Debes poder: identificar la carpeta raíz, ejecutar el Python de .venv, observar los cinco escenarios de demo.py y obtener 173 passed con retorno 0. Si usaste Docker, comprueba además 115 passed y el JSON de entorno aislado. Si ejecutaste agentes, conserva los cuatro entregables y las decisiones humanas reales.

No se requiere instalar las herramientas de autoría del informe o las diapositivas para ejecutar el evaluador. Los comandos básicos se revisaron contra el código de entrega; las instalaciones gráficas dependen de cada sistema. Documento actualizado el 21 de noviembre de 2026.

Fuentes oficiales de instalación: [Python](https://www.python.org/downloads/), [Git](https://git-scm.com/install/), [VS Code](https://code.visualstudio.com/download), [Docker](https://docs.docker.com/desktop/). Las reglas y resultados esperados proceden del código, plan y pruebas de [E4-LLM](https://github.com/lukasscheelb/E4-LLM/tree/entrega-3).
