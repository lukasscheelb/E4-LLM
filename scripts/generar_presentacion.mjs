import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {spawnSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
const ROOT=process.cwd();
const MODULES=process.env.MIRA_RUNTIME_NODE_MODULES;
const RUNTIME_PYTHON=process.env.MIRA_RUNTIME_PYTHON;
const SKILL=process.env.MIRA_PRESENTATION_SKILL_DIR;
if(!MODULES||!RUNTIME_PYTHON||!SKILL) throw new Error('Configura MIRA_RUNTIME_NODE_MODULES, MIRA_RUNTIME_PYTHON y MIRA_PRESENTATION_SKILL_DIR con las dependencias del entorno de autoría.');
process.env.RUNTIME_NODE_MODULES ??= MODULES;
const req=createRequire(path.join(MODULES,'resolve.mjs'));
const {Presentation,PresentationFile}=await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const pres=Presentation.create({slideSize:{width:1280,height:720}});
const dir=path.join(ROOT,'tmp/entrega/slides');await fs.mkdir(dir,{recursive:true});
function txt(s,text,x,y,w,h,size=26,bold=false,color='#263648'){
 const el=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 el.text=text;el.text.style={fontFamily:'Arial',fontSize:`${size}pt`,bold,color};el.text.insets=0;return el;
}
function slide(title,note){const s=pres.slides.add();s.background.fill='#FAFBFD';txt(s,title,72,58,1136,105,32,true,'#142D4E');s.speakerNotes.text=note;return s;}
const source='Fuente: repositorio E4-LLM, revisión 08f0bbf, docs/bitacora.md, docs/trabajo/revision.md y docs/linea-base/comparacion.md. ';
let s=slide('MIRA E4\nSistema multiagente',source+'Lukas. 40 segundos. Presentar alternativa A y equipo. Identificar los cuatro roles como agentes de Codex y describir el entorno Python de pruebas.');
txt(s,'Desarrollo conducido por especificación',72,290,1136,70,26);
txt(s,'Lukas Scheel · Representante de negocio\nFrancisca Meyer\nSebastian Rodriguez',72,405,1136,170,22);
s=slide('Evaluación de casos MIRA',source+'Lukas. 80 segundos. Explicar que el puntaje ya llega calculado, las tres rutas y el rechazo humano.');
txt(s,'Puntaje recibido y configuración por organización',72,205,1136,95,28,true);
txt(s,'Fraude o riesgo alto: supervisor\nSeñal faltante o mínimo incumplido: revisión\nCaso sin alertas desde el corte: aprobación',72,330,1136,225,26);
txt(s,'Python local y pytest. Sin Bonsai ni servicios externos.',72,595,1136,55,19);
s=slide('Cuatro roles y archivos de traspaso',source+'Francisca. 75 segundos. Explicar cada rol y dos puntos humanos. Diagrama editable. Máximo dos ciclos si Reviewer rechaza, cero usados.');
txt(s,'Agentes de Codex con responsabilidades separadas',72,180,1136,45,22);
const roles=[['Analista','analisis.md'],['Planificador','plan.md'],['Developer','src y evidencia'],['Reviewer','revision.md']];
for(let i=0;i<4;i++){let x=72+i*293;s.shapes.add({geometry:'rect',position:{left:x,top:250,width:230,height:100},fill:'#E3EBF3',line:{fill:'#8EA1B7',width:1}});txt(s,roles[i][0],x+16,270,205,40,23,true);txt(s,roles[i][1],x+16,315,205,35,17);if(i<3)s.shapes.add({geometry:'rightArrow',position:{left:x+244,top:282,width:35,height:25},fill:'#64748B',line:{fill:'none',width:0}});}
txt(s,'Control humano 1: especificación aprobada antes del código\nControl humano 2: revisión y autorización del plan',72,425,1136,135,24);
s=slide('Skills y límites de herramientas',source+'Francisca. 60 segundos. Skills realmente leídas y aplicadas, no solo citadas. Explicar los límites de cada rol y su cumplimiento mediante instrucciones.');
txt(s,'generar-criterios\nPlantilla de condiciones, fronteras y colisiones',72,190,1136,105,24);
txt(s,'verificar-trazabilidad\nRequisito, diseño, código y prueba en ambos sentidos',72,335,1136,105,24);
txt(s,'pytest-runner\nScript ejecutable y retorno real del mismo intérprete',72,480,1136,105,24);
s=slide('Aprobaciones y trazabilidad',source+'Francisca. 45 segundos. Mostrar hashes de bitácora. Identificar la aprobación expresa del representante.');
txt(s,'2c625d6   Revisión documental\ncadb048   Registro de aprobación de Lukas\n30c7d65   Plan y addendum\n5a7b12d   Autorización humana de Developer',72,205,1136,280,26);
txt(s,'Cada resultado identifica el código que se probó',72,570,1136,60,24,true);
s=slide('Demostración del flujo',source+'Sebastian. 360 segundos. Seguir docs/entrega/guion-demo.md. Abrir etiqueta entrega-3, necesidad, análisis, plan y aprobación. Ejecutar python scripts/demo.py y pytest mediante Skill. Mostrar colisión, errores, aislamiento y veredicto. Una repetición de pruebas no se presenta como nueva corrida de agentes. Si arranque de agentes excede tiempo, lanzar en vivo y mostrar finales guardados conforme pauta.');
txt(s,'1  Necesidad, análisis y decisiones aprobadas\n2  Plan y autorización del representante\n3  API y casos de frontera, fraude y errores\n4  pytest, evidencia sin red y Reviewer',72,200,1136,290,28);
txt(s,'La guía distingue reproducción del producto y nueva corrida de agentes',72,565,1136,80,20);
s=slide('Ambas soluciones cumplen la aceptación',source+'Sebastian. 60 segundos. Misma suite posterior e imagen sin red. Las suites propias tienen tamaños distintos. No inferir calidad por conteo.');
const values=[['Comprobación','Multiagente','Generalista'],['Suite propia','173 / 173','124 / 124'],['Suite común sin red','115 / 115','115 / 115'],['Criterios verificados','17 / 17','17 / 17'],['Requisitos cubiertos','8 / 8','8 / 8']];
const tb=s.tables.add({rows:5,columns:3,left:72,top:190,width:1136,height:330,values,columnWidths:[526,305,305]});
for(let r=0;r<5;r++)for(let c=0;c<3;c++){const cell=tb.getCell(r,c);cell.text.style={fontFamily:'Arial',fontSize:'21pt',bold:r===0,color:r===0?'#FFFFFF':'#263648'};cell.fill=r===0?'#142D4E':(r%2?'#EEF2F6':'#FFFFFF');}
tb.borders.assign({fill:'#CBD5E1',width:1});
txt(s,'Una corrida y evaluación posterior. Sin evidencia de ahorro de costo.',72,575,1136,70,21);
s=slide('Incidencias y correcciones observadas',source+'Francisca. 50 segundos. MAST como interpretación, no certificación. F01 posible entrega tardía. F02 error de evaluación no de lógica baseline. Fuente taxonomía: https://arxiv.org/html/2503.13657v2.');
txt(s,'Aporte de catálogo no incorporado en la primera salida\nSegundo turno y addendum. Posible FM-2.5, con incertidumbre.',72,200,1136,145,24);
txt(s,'La comparación importó el módulo de otro checkout\nConfiguración explícita y verificación de ruta. Compatible con FM-3.3.',72,395,1136,145,24);
txt(s,'Logs originales conservados. Las clasificaciones no sustituyen evidencia causal.',72,595,1136,60,18);
s=slide('Lo que esta corrida permite concluir',source+'Lukas. 80 segundos. Explicar por qué no se inventan tokens/tiempos y controles reales. No afirmar corrección humana que no ocurrió.');
txt(s,'La separación hizo visibles decisiones y responsabilidades',72,205,1136,95,28,true);
txt(s,'El generalista alcanzó el mismo resultado funcional\nFaltan tiempos y tokens completos comparables\nLa suite común se creó después de las implementaciones',72,350,1136,220,25);
s=slide('Aprendizajes y siguiente iteración',source+'Sebastian. 50 segundos. Cierre. Todo equipo debe dominar código, skills y permisos. 15 minutos total. Reservar 5 minutos preguntas fuera de presentación.');
txt(s,'Aprobación concreta antes de implementar\nIdentidad del código antes de aceptar pruebas\nMedición simétrica desde el primer despacho',72,210,1136,250,29);
txt(s,'Repositorio y evidencia verificables\ngithub.com/lukasscheelb/E4-LLM',72,540,1136,100,21);
for(let i=0;i<pres.slides.items.length;i++){const blob=await pres.export({slide:pres.slides.items[i],format:'png',scale:1});await fs.writeFile(path.join(dir,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));}
const candidate=path.join(ROOT,'tmp/entrega/candidate.pptx');await(await PresentationFile.exportPptx(pres)).save(candidate);
const metadata=spawnSync(RUNTIME_PYTHON,[path.join(ROOT,'scripts/normalizar_propiedades_presentacion.py'),candidate],{encoding:'utf-8'});
if(metadata.status!==0) throw new Error(metadata.stderr||'No se normalizaron propiedades');
const final=process.env.MIRA_PPTX_OUT || path.join(ROOT,'output/presentacion/Presentacion_MIRA_E4.pptx');
await fs.mkdir(path.dirname(final),{recursive:true});
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath:final,pythonExecutable:RUNTIME_PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','7'],requiredNativeTableOwnerSlides:[7],fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,explicitTotalSlideCount:10,receiptPath:process.env.MIRA_PPTX_RECEIPT || path.join(ROOT,`tmp/entrega/validacion-pptx-${Date.now()}.json`)});
console.log(JSON.stringify(result));
