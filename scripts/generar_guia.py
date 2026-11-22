"""Renderiza la guía de instalación desde su fuente JSON versionada."""
from pathlib import Path
import json,re,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Preformatted,Table,TableStyle,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(TTFont('Arial',r'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold',r'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Code',r'C:/Windows/Fonts/consola.ttf'))
styles={
 'p':ParagraphStyle('p',fontName='Arial',fontSize=10,leading=14,spaceAfter=11),
 'h':ParagraphStyle('h',fontName='ArialBold',fontSize=12.2,leading=16,spaceBefore=9,spaceAfter=9,keepWithNext=True),
 'title':ParagraphStyle('title',fontName='ArialBold',fontSize=20,leading=25,spaceAfter=16),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=8.7,leading=11.5),
 'code':ParagraphStyle('code',fontName='Code',fontSize=8.1,leading=10.4,spaceBefore=3,spaceAfter=13,leftIndent=8,rightIndent=8,backColor=colors.HexColor('#F1F5F9'),borderPadding=8),
}
def markup(text):
 safe=html.escape(text)
 return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<a href="{m[2]}" color="#1759A8">{m[1]}</a>',safe)
d=json.loads((ROOT/'docs/entrega/guia-instalacion.json').read_text(encoding='utf-8'))
story=[]
for i,pg in enumerate(d['pages']):
 story.append(Paragraph(pg['title'],styles['title']))
 for item in pg['items']:
  kind=item['type']
  if kind in ['p','h']:story.append(Paragraph(markup(item['text']),styles[kind]))
  elif kind=='code':
   assert max(map(len,item['text'].splitlines()))<=100
   story.append(Preformatted(item['text'],styles['code']))
  else:
   rows=[[Paragraph(markup(x),styles['cell']) for x in r] for r in item['rows']]
   t=Table(rows,colWidths=item.get('widths') or [150,361],repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDE7F1')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#CBD5E1')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
   story += [t,Spacer(1,12)]
 if i<len(d['pages'])-1:story.append(PageBreak())
def header(c,doc):
 c.setFillColor(colors.HexColor('#64748B'));c.setFont('Arial',8)
 c.drawString(42,816,'MIRA E4 · Instalación y ejecución desde cero')
 c.drawRightString(553,25,str(doc.page))
out=ROOT/'output/pdf/Guia_Instalacion_MIRA_E4.pdf'
SimpleDocTemplate(str(out),pagesize=(595,842),leftMargin=42,rightMargin=42,topMargin=48,bottomMargin=42,title=d['title'],author='Equipo MIRA E4').build(story,onFirstPage=header,onLaterPages=header)
print(out)
