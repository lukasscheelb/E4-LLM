"""Genera el informe PDF desde el contenido verificable versionado."""
from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Flowable,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('Arial',r'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold',r'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyM',fontName='Arial',fontSize=10.4,leading=15,spaceAfter=12))
styles.add(ParagraphStyle(name='HeadM',fontName='ArialBold',fontSize=19,leading=24,spaceAfter=18))
styles.add(ParagraphStyle(name='SmallM',fontName='Arial',fontSize=8.1,leading=11,spaceAfter=4))
styles.add(ParagraphStyle(name='CoverM',fontName='ArialBold',fontSize=29,leading=36,spaceAfter=24))
D=json.loads((ROOT/'docs/entrega/contenido.json').read_text(encoding='utf-8'))
W=511
class Diagram(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=W;self.height=222
 def draw(self):
  c=self.canv
  nodes=[('Analista','analisis.md',10,150),('Planificador','plan.md',272,150),('Developer','src, tests y evidencia',10,30),('Reviewer','revision.md',272,30)]
  for name,sub,x,y in nodes:
   c.setFillColor(colors.HexColor('#F1F5F9'));c.setStrokeColor(colors.HexColor('#64748B'));c.roundRect(x,y,225,58,5,fill=1,stroke=1)
   c.setFillColor(colors.HexColor('#142D4E'));c.setFont('ArialBold',12);c.drawString(x+12,y+36,name)
   c.setFont('Arial',9);c.drawString(x+12,y+17,sub)
  c.setStrokeColor(colors.HexColor('#475569'))
  for x1,y1,x2,y2 in [(235,179,272,179),(384,150,384,118),(384,118,122,118),(122,118,122,88),(235,59,272,59)]:c.line(x1,y1,x2,y2)
  c.setFont('Arial',8);c.setFillColor(colors.black)
  c.drawString(4,214,'H1: aprobación documental previa   2c625d6 / cadb048')
  c.drawString(135,104,'H2: autorización humana del plan   30c7d65 / 5a7b12d')
  c.drawString(14,8,'Si Reviewer rechaza: máximo dos ciclos de corrección. Corrida real: cero.')
def P(text,small=False):
 return Paragraph(text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('&lt;br/&gt;', '<br/>'),styles['SmallM' if small else 'BodyM'])
def table(rows,widths):
 t=Table([[P(str(x),True) for x in r] for r in rows],colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDE7F1')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 return t
story=[Spacer(1,95),Paragraph('MIRA E4<br/>Diseño y ejecución de un sistema multiagente',styles['CoverM']),P('Alternativa A · Desarrollo conducido por especificación'),Spacer(1,25),P('Lukas Scheel · Representante de negocio<br/>Francisca Meyer<br/>Sebastian Rodriguez'),Spacer(1,28),P('Taller de Desarrollo de Software Conducido por Agentes de IA<br/>Universidad de Valparaíso<br/>21 de noviembre de 2026'),Spacer(1,36),P('Sistema de cuatro agentes con responsabilidades separadas.<br/>Pruebas: Python 3.14.3 / 3.14.10, pytest 9.0.2, Docker 29.9.2.'),P('Entrega funcional: 17 criterios verificados. Los límites experimentales y las verificaciones humanas pendientes se declaran en el informe.'),PageBreak()]
for i,p in enumerate(D['pages']):
 story.append(Paragraph(p['section']+' '+p['title'],styles['HeadM']))
 if p.get('diagram'):story += [Diagram(),Spacer(1,15)]
 if p.get('roles'):story += [table([['Rol','Herramientas','Entrada','Salida','Término','Skill']]+D['roles'],[66,69,85,95,86,110]),Spacer(1,16)]
 if p.get('results'):story += [table([['Comprobación','Multiagente','Generalista'],['Suite propia local','173/173','124/124'],['Suite común sin red','115/115','115/115'],['Criterios / requisitos','17/17 y 8/8','17/17 y 8/8'],['Revisión','Reviewer independiente','Autoevaluación'],['Tiempo total comparable','No disponible','No disponible'],['Tokens / permisos completos','No disponibles','No disponibles']],[241,135,135]),Spacer(1,16)]
 for text in p['paragraphs']:story.append(P(text))
 if p.get('timeline'):story += [Spacer(1,8),table([['Hito','Commit']]+p['timeline'],[350,161])]
 if p.get('second_title'):
  story += [Spacer(1,10),Paragraph(p['second_section']+' '+p['second_title'],styles['HeadM'])]
  for text in p['second_paragraphs']:story.append(P(text))
 if i<len(D['pages'])-1:story.append(PageBreak())
def header(c,doc):
 c.setFont('Arial',8);c.setFillColor(colors.HexColor('#64748B'))
 c.drawString(42,815,'MIRA E4 · Sistemas multiagente')
 c.drawRightString(553,25,str(doc.page))
path=ROOT/'output/pdf/Informe_MIRA_E4.pdf'
SimpleDocTemplate(str(path),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=48,bottomMargin=45,title='MIRA E4 Diseño y ejecución del sistema multiagente',author='Lukas Scheel; Francisca Meyer; Sebastian Rodriguez').build(story,onFirstPage=header,onLaterPages=header)
print(path)
