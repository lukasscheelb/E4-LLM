import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {spawnSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
const ROOT=process.cwd(), MODULES=process.env.MIRA_RUNTIME_NODE_MODULES;
const PY=process.env.MIRA_RUNTIME_PYTHON, SKILL=process.env.MIRA_PRESENTATION_SKILL_DIR;
if(!MODULES||!PY||!SKILL)throw Error('Configura las tres variables MIRA del entorno de autoría.');
process.env.RUNTIME_NODE_MODULES ??= MODULES;
const req=createRequire(path.join(MODULES,'resolve.mjs'));
const {Presentation,PresentationFile}=await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const pres=Presentation.create({slideSize:{width:1280,height:720}});
const C={ink:'#24333B',muted:'#596970',salmon:'#B85647',dark:'#78372D',pale:'#FFF3EF',line:'#D5A295',soft:'#FBE1D9',white:'#F7C4B9',teal:'#456D73'};
const build=path.join(ROOT,'tmp/presentacion-salmon-10');await fs.mkdir(build,{recursive:true});
const timings=[25,95,85,95,80,170,110,90,90,60];
const speakers=['Lukas','Lukas','Francisca','Francisca','Sebastian','Sebastian','Sebastian','Sebastian','Francisca','Lukas'];
function shape(s,x,y,w,h,fill=C.salmon,geometry='rect',stroke='none'){return s.shapes.add({geometry,position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:stroke==='none'?0:1}});}
function t(s,text,x,y,w,h,size=20,bold=false,color=C.ink){const el=shape(s,x,y,w,h,'none','textbox');el.text=text;el.text.style={fontFamily:'Arial',fontSize:`${size}pt`,bold,color};el.text.insets=0;return el;}
function rule(s,x,y,w,color=C.line){shape(s,x,y,w,2,color);}
function arrow(s,x,y,w=30,color=C.salmon){shape(s,x,y,w,18,color,'rightArrow');}
function down(s,x,y,h=30,color=C.salmon){shape(s,x,y,18,h,color,'downArrow');}
function base(title,source,note='',appendix=false){const s=pres.slides.add(),i=pres.slides.items.length;s.background.fill=C.white;
 shape(s,64,44,50,6,C.salmon);t(s,title,64,72,1152,84,31,true);
 rule(s,64,660,1152);t(s,appendix?'MIRA E4   Anexo técnico':'MIRA E4   Desarrollo conducido por especificación',64,679,1000,22,10,false,C.muted);t(s,String(i).padStart(2,'0'),1176,675,40,27,12,true,C.dark);
 s.speakerNotes.text=`${appendix?'Anexo para preguntas.':speakers[i-1]+'. '+timings[i-1]+' segundos.'}\n${note}\nFuentes del repositorio: ${source}.\nPauta docente, sección 7 y rúbrica 9.2. Las notas son apoyo de preparación y no acreditan ensayo oral.`;return s;}
function table(s,values,x,y,w,h,widths,size=16){const tb=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,values,columnWidths:widths});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=tb.getCell(r,c);cell.fill=r===0?C.pale:(r%2?C.white:C.soft);cell.text.style={fontFamily:'Arial',fontSize:`${size}pt`,bold:r===0,color:r===0?C.dark:C.ink};}tb.borders.assign({fill:C.line,width:1});return tb;}
function note(s,text,y=606){t(s,text,64,y,1152,42,13,false,C.muted);}
function metric(s,value,label,x,y,w=300){t(s,value,x,y,w,80,46,true,C.dark);t(s,label,x,y+88,w,64,17,false,C.muted);}
let s=base('MIRA E4','docs/decision.md y docs/entrega/agentes.md','Presentar al equipo, alternativa A y resultado funcional. El puntaje llega calculado. Herramienta de los cuatro roles: Codex. Identificador exacto del modelo y versión de la app no expuestos.');
// Cover: typography and a simple branching motif, all native editable objects.
t(s,'Evaluación de casos\ncon cuatro agentes',64,190,800,180,43,true);
t(s,'Especificación aprobada, implementación local\ny evidencia verificable',64,397,790,100,23,false,C.muted);
t(s,'Lukas Scheel, representante de negocio\nFrancisca Meyer y Sebastian Rodriguez',64,552,850,65,17);
shape(s,1040,230,86,86,C.pale,'ellipse');shape(s,1040,400,86,86,C.salmon,'ellipse');shape(s,1170,315,38,38,C.ink,'ellipse');shape(s,1079,316,7,84,C.salmon);arrow(s,1128,334,40);t(s,'A',1066,251,40,40,24,true,C.dark);t(s,'E4',1056,422,65,40,22,true,'#FFFFFF');

s=base('El caso y el alcance aprobado','docs/trabajo/analisis.md, docs/trabajo/plan.md y src/mira/evaluador.py','Elegimos A porque permite validar reglas de negocio con fronteras y colisiones observables. Explicar el cambio respecto del enunciado ilustrativo: MIRA recibe puntaje, no lo calcula, y no rechaza automáticamente. Decisiones P-01 a P-09 y tres aclaraciones.');
t(s,'Necesidad del cliente',64,185,500,40,21,true,C.dark);t(s,'Clasificar cada caso según\nsu organización y las alertas',64,244,540,112,26,true);
t(s,'Salida de negocio',700,185,510,40,21,true,C.dark);t(s,'Aprobación automática\nRevisión asistida\nEscalamiento al supervisor',700,244,510,155,25);
rule(s,64,429,1152);
t(s,'Contrato de decisión',64,455,1152,40,22,true,C.dark);
t(s,'Fraude activo o puntaje < R: escalamiento\nAusencia, mínimo incumplido o R ≤ puntaje < A: revisión\nSin alertas y puntaje ≥ A: aprobación',64,508,1152,115,20);

s=base('Arquitectura y controles humanos','docs/decision.md, docs/bitacora.md y docs/trabajo/','Patrón efectivo: especialistas secuenciales coordinados con archivos. Traspasos automáticos del coordinador, con dos aprobaciones humanas. Se descartó el orquestador como rol por dependencias lineales, mayor enrutamiento y mismo riesgo de saltar aprobaciones. Máximo dos ciclos Developer–Reviewer tras rechazo. Cero usados.');
t(s,'Cuatro agentes de Codex, separados por responsabilidad',64,162,1152,42,19,false,C.muted);
const names=['Analista','Planificador','Developer','Reviewer'];const files=['analisis.md','plan.md','src/ + tests/','revision.md'];
for(let i=0;i<4;i++){const x=64+i*302;shape(s,x,278,246,132,i===2?C.pale:C.soft,'rect',C.line);t(s,names[i],x+17,300,218,40,23,true);t(s,files[i],x+17,355,220,35,16,false,C.muted);if(i<3)arrow(s,x+259,334,30);}
shape(s,64,214,246,41,C.salmon);t(s,'Aprobación documental',77,222,225,28,14,true,C.ink);shape(s,366,214,246,41,C.salmon);t(s,'Autorización del plan',379,222,225,28,14,true,C.ink);
t(s,'Traspasos por archivos en docs/trabajo/',64,445,600,40,21,true);t(s,'Cada etapa consume una salida concreta\ny conserva la revisión que recibió',64,494,610,88,20,false,C.muted);
t(s,'Revisión con retorno acotado',790,445,426,40,21,true,C.dark);t(s,'Máximo: 2 ciclos de corrección\nCorrida entregada: 0 ciclos',790,494,426,86,20);
note(s,'Secuencia por dependencias lineales. Se descartó un orquestador como rol por costo de enrutamiento y control.');

s=base('Contratos y herramientas por agente','docs/entrega/agentes.md y .github/agents/*.agent.md','Justificar edición del Analista para borradores, ejecución del Developer para Git y pytest, y solo lectura del Reviewer para independencia. Planificador y Reviewer devuelven texto que el coordinador guarda. Los límites fueron por instrucciones, no sandbox técnico de herramientas.');
table(s,[['Rol y herramientas','Contrato de salida','Skill aplicada'],['Analista\nread, search, edit','analisis.md\n17 CA contrastados o duda explícita','generar-criterios\nPlantilla de condiciones y fronteras'],['Planificador\nread, search','plan.md\nDiseño y prueba por cada CA','verificar-trazabilidad\nMatriz bidireccional'],['Developer\nread, search, edit, execute','API, tests y evidencia\nAprobación verificada y pytest real','pytest-runner\nScript con mismo intérprete y retorno'],['Reviewer\nread, search','revision.md\nVeredicto trazable, sin editar','verificar-trazabilidad\nContraste de código y evidencia']],64,181,1152,375,[320,405,427],16);
note(s,'Edición para análisis y código. Ejecución solo en Developer. Restricciones por instrucciones de rol.',625);

s=base('Demostración en vivo: entrada y traspasos','docs/entrega/guion-demo.md, docs/bitacora.md y README.md','Este bloque inicia la demo de seis minutos, repartida entre diapositivas 5–7. Ejecutar sobre entrega-3 en copia preparada. Lanzar Analista con perfil y generar-criterios desde la necesidad original. Mostrar carga, salida y traspaso. Si el flujo supera el tiempo, mostrar finales entregados consistentes con la etiqueta, como permite la pauta. Identificar la aprobación real de Lukas sin fingir una nueva.');
t(s,'Etiqueta entrega-3, entorno preparado',64,170,1152,50,25,true,C.dark);
const timeline=[['Necesidad y aclaraciones','2c625d6','Especificación e historia'],['Aprobación del representante','cadb048','Registro independiente'],['Plan y addendum','30c7d65','Diseño y seis opcionales'],['Autorización de Developer','5a7b12d','Control adicional del plan']];
timeline.forEach((r,i)=>{const y=253+i*79;shape(s,69,y+5,15,15,C.salmon,'ellipse');if(i<3)shape(s,75,y+20,3,59,C.line);t(s,r[0],110,y,520,45,21,true);t(s,r[1],660,y,175,40,20,true,C.dark);t(s,r[2],853,y,360,45,17,false,C.muted);});
note(s,'La demo debe mostrar un agente y su skill en uso. scripts/demo.py reproduce únicamente el producto.');

s=base('Contrato de la API y casos de frontera','src/mira/evaluador.py y scripts/demo.py','Parte de la demo. Ejecutar python scripts/demo.py. La función es evaluar_caso(caso, configuraciones), sin servidor HTTP. Valores numéricos int estrictos, bool explícito para fraude, sin coerciones. Demostrar 84,85,59, colisión fraude/mínimo/ausencia e indicador omitido. Explicar motivo principal y trazabilidad de configuración.');
t(s,'evaluar_caso(caso, configuraciones)',64,169,1152,48,25,true,C.dark);
shape(s,64,239,520,320,C.soft);t(s,'Entrada',86,258,470,34,20,true);t(s,'organizacion: "X"\npuntaje: 85\nsenales: numéricas y fraude\n\nconfiguraciones["X"]\nid, version, R: 60, A: 85',86,311,470,230,18);
arrow(s,612,374,52);
shape(s,700,239,516,320,C.pale);t(s,'Salida',722,258,470,34,20,true);t(s,'ok y decision\nmotivo_principal y motivos\ndesglose por señal\nconfiguracion aplicada\n\nError: tipo, codigo, campo, mensaje',722,311,470,230,18);
t(s,'84: revisión      85: aprobación      59: escalamiento',64,589,1152,43,22,true);

s=base('Verificación del producto y del entorno','docs/trabajo/revision.md, docs/evidencia/cierre-multi-entorno.json, docs/evidencia/entorno_aislado.py y docs/evidencia/*junit.xml','Parte final de la demo. Ejecutar python .github/skills/pytest-runner/scripts/run_pytest.py tests. Mostrar retorno, JUnit, manifiesto y Reviewer. Si se repite Docker, conservar un log nuevo sin sobrescribir históricos. Aislamiento CA-10 real: red none, interfaz lo, sin rutas y TCP rechazado Errno101. No confundir reproducir tests con una nueva corrida multiagente.');
metric(s,'173/173','Suite propia del Developer',64,184,340);metric(s,'17/17','Criterios de aceptación',472,184,340);metric(s,'0','Hallazgos P1/P2 del Reviewer',884,184,330);
rule(s,64,380,1152);t(s,'Aislamiento real',64,412,485,43,25,true,C.dark);t(s,'Docker con NetworkMode=none\nSolo interfaz lo y sin rutas externas\nTCP rechazada con Errno 101',64,477,540,118,21);
t(s,'Integridad y revisión',700,412,516,43,25,true,C.dark);t(s,'Hash del estado probado y JUnit\nGuardia del origen del módulo\nReviewer separado y solo lectura',700,477,516,118,21);

s=base('Mismo cumplimiento en la suite común','docs/linea-base/comparacion.md y docs/evidencia/cierre-*-junit.xml','Métrica del gráfico: pruebas aprobadas de las mismas 115. Ambos obtienen 115/115, 17/17 CA y 8/8 requisitos. Suites propias 173 y124 distintas: no compararlas como calidad. Baseline generalista nuevo sin historial ni delegación, desde cadb048, commit79c69fd. Misma imagen Python3.14.10 pytest9.0.2 sin red. Suite común posterior, no ciega.');
t(s,'Pruebas aprobadas de 115 comprobaciones comunes',64,162,1152,37,18,false,C.muted);
s.charts.add('bar',{position:{left:64,top:222,width:720,height:355},categories:['Multiagente','Generalista'],series:[{name:'Pruebas aprobadas',values:[115,115],fill:C.dark,points:[{idx:1,fill:C.teal}]}],barOptions:{direction:'column',grouping:'clustered',gapWidth:130},hasLegend:false,chartFill:C.white,plotAreaFill:C.white,xAxis:{textStyle:{typeface:'Arial',fontSize:18,fill:C.ink},line:{fill:C.line,width:1}},yAxis:{min:0,max:125,majorUnit:25,numberFormatCode:'0',textStyle:{typeface:'Arial',fontSize:14,fill:C.muted},majorGridlines:{fill:C.line,width:1}},dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:'Arial',fontSize:24,bold:true,fill:C.ink}}});
t(s,'17/17 CA   8/8 requisitos',825,222,390,58,22,true,C.dark);
t(s,'Complemento del 22/11',825,303,390,42,19,true);
t(s,'Mediana de pytest, 3 repeticiones\nMultiagente: 1,254 s\nGeneralista: 1,244 s',825,363,390,135,18);
t(s,'114 pruebas funcionales\nCA-10 excluido en Windows',825,510,390,65,16,false,C.muted);
note(s,'Suite común histórica sin red: 115/115. Medición posterior de pytest: sin ventaja inferible ni costo total medido.');
s.speakerNotes.text+='\nComplemento: docs/linea-base/comparacion.md y docs/evidencia/verificacion-comparable-2026-11-22.json. Tres repeticiones alternadas por enfoque con 114 aprobadas y una deseleccionada. Medianas de pared 1,254 y 1,244 s. Son tiempos de pytest, no de desarrollo. Tokens completos ausentes.';

s=base('Fallas reales y correcciones conservadas','docs/entrega/fallas.md, docs/evidencia/cierre-prevencion.diff y docs/evidencia/cierre-planificador.md','P3 exige una falla real con corrección, sin maquillar. Se muestran dos con límites MAST. Interpretación histórica basada en Cemri et al., Why Do Multi-Agent LLM Systems Fail?, arXiv2503.13657v2, https://arxiv.org/html/2503.13657v2. F01 posible FM-2.5, entrega tardía no descartada. F02 compatible FM-3.3 en evaluación posterior, no defecto del producto. Dif y repetición sí existen, causalidad plena a una línea no acreditada.');
t(s,'Falla de evaluación',64,184,550,50,25,true,C.dark);
t(s,'pytest cargó el módulo de otro checkout\n114 fallos inválidos para medir la lógica\nConfiguración explícita y guardia de ruta',64,257,550,145,21);
t(s,'Repetición: 115/115 en ambas soluciones\nCompatible con FM-3.3, interpretación MAST',64,436,550,105,18,false,C.muted);
shape(s,638,185,2,380,C.line);
t(s,'Devolución humana del 22/11',690,184,526,65,24,true,C.dark);
t(s,'Observación: faltaba la ruta del módulo\nEl usuario devolvió la evidencia\nNueva ejecución verificó mira.__file__',690,277,526,145,21);
t(s,'173/173, retorno 0, sin cambiar el código\nEvidencia complementaria, cierre pendiente',690,457,526,96,18,false,C.muted);
note(s,'F-01 adicional: catálogo omitido, addendum e inventario de aportes. Clasificación y límites en las notas.');
s.speakerNotes.text+='\nActualización complementaria: docs/trabajo/revision-vscode.md. Decisión humana literal: Devolver para corregir la evidencia. Nuevo log vscode-developer-r1.log y JUnit 173 aprobadas. No convierte retrospectivamente la corrida original en una corrección humana. Disponible para revisión de cierre.';

s=base('Aprendizajes y próxima iteración','docs/entrega/informe.md, docs/decision.md y docs/evidencia/cierre-prevencion.diff','Cerrar en un minuto. Aprendizajes: contrato observable, aprobación concreta y estado probado. Próxima corrida: instrumentación simétrica, suite congelada antes y registro humano real. Exponen los tres. Reservar5min para preguntas. No afirmar que este deck acredita ensayo, participación o demo realizada.');
t(s,'Contratos claros',64,200,345,50,27,true,C.dark);t(s,'Cada rol entrega un artefacto\ny termina con evidencia',64,280,345,117,23);
t(s,'Control humano concreto',462,200,350,90,27,true,C.dark);t(s,'Una revisión identificable\nantes de habilitar código',462,321,350,117,23);
t(s,'Medición desde el inicio',862,200,354,90,27,true,C.dark);t(s,'Suite común previa, tiempos\ny tokens con igual ventana',862,321,354,117,23);
rule(s,64,510,1152,C.salmon);t(s,'Aceptación funcional en ambos enfoques',64,548,1152,45,26,true);t(s,'Sin ahorro demostrado de tiempo total o tokens. Suite común posterior y no ciega.',64,605,1152,35,15,false,C.muted);

for(let i=0;i<pres.slides.items.length;i++){const blob=await pres.export({slide:pres.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));}
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(pres)).save(candidate);
const meta=spawnSync(PY,[path.join(ROOT,'scripts/normalizar_propiedades_presentacion.py'),candidate],{encoding:'utf-8'});if(meta.status!==0)throw Error(meta.stderr);
const final=process.env.MIRA_PPTX_OUT||path.join(build,`final-${Date.now()}/Presentacion_MIRA_E4.pptx`);
await fs.mkdir(path.dirname(final),{recursive:true});
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,pythonExecutable:PY,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','4'],requiredNativeTableOwnerSlides:[4],fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,materializeLiteralChartWorkbooks:true,explicitTotalSlideCount:10,receiptPath:process.env.MIRA_PPTX_RECEIPT||path.join(build,`validacion-${Date.now()}.json`)});
if(!process.env.MIRA_PPTX_OUT){const published=path.join(ROOT,'output/presentacion/Presentacion_MIRA_E4.pptx');await fs.mkdir(path.dirname(published),{recursive:true});await fs.copyFile(final,published);}
console.log(JSON.stringify(result));
