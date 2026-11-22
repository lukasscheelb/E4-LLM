"""Demostración reproducible del producto; no sustituye la corrida de agentes."""
from pathlib import Path
import sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from mira import evaluar_caso
base={'organizacion':'X','puntaje':85,'senales':{'DOC_AUT':70,'BIO_ROSTRO':75,'CRUCE_MONTO':60,'CRUCE_FECHA':60,'FRA_EDICION':False,'FRA_MEMORIA':False,'FRA_SINTETICO':False}}
configs={'X':{'id':'X-v1','version':'1','R':60,'A':85}}
scenarios=[]
for score in [84,85,59]:
 c=copy.deepcopy(base);c['puntaje']=score;scenarios.append((f'Puntaje {score}',c))
c=copy.deepcopy(base);c['senales']['FRA_EDICION']=True;c['senales']['DOC_AUT']=69;del c['senales']['BIO_ROSTRO'];scenarios.append(('Fraude, mínimo y ausencia',c))
c=copy.deepcopy(base);del c['senales']['FRA_MEMORIA'];scenarios.append(('Indicador de fraude omitido',c))
for label,case in scenarios:
 print('\n'+label)
 print(json.dumps(evaluar_caso(case,configs),ensure_ascii=False,indent=2))
