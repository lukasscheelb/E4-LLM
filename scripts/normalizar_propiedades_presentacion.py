"""Normaliza propiedades de publicación sin alterar el contenido de las diapositivas."""
from pathlib import Path
import sys,zipfile,xml.etree.ElementTree as E
p=Path(sys.argv[1])
with zipfile.ZipFile(p) as z:entries=[(i,z.read(i.filename)) for i in z.infolist()]
ns={'dc':'http://purl.org/dc/elements/1.1/','cp':'http://schemas.openxmlformats.org/package/2006/metadata/core-properties','ap':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
for key,value in ns.items():E.register_namespace(key,value)
E.register_namespace('a','http://schemas.openxmlformats.org/drawingml/2006/main')
result=[]
for info,data in entries:
 name=info.filename
 if name=='docProps/core.xml':
  root=E.fromstring(data)
  for tag in [f"{{{ns['dc']}}}creator",f"{{{ns['cp']}}}lastModifiedBy"]:
   for node in root.findall(tag):root.remove(node)
  title=root.find(f"{{{ns['dc']}}}title")
  if title is not None:title.text='MIRA E4 Sistema multiagente'
  data=E.tostring(root,encoding='utf-8',xml_declaration=True)
 elif name=='docProps/app.xml':
  root=E.fromstring(data)
  for node in root.findall(f"{{{ns['ap']}}}Application"):root.remove(node)
  for key,value in [('Slides','10'),('Notes','10'),('PresentationFormat','Presentación')]:
   node=root.find(f"{{{ns['ap']}}}{key}")
   if node is not None:node.text=value
  data=E.tostring(root,encoding='utf-8',xml_declaration=True)
 elif name.endswith('.xml') and '/theme/' in name:
  root=E.fromstring(data)
  for node in root.iter():
   if node.get('name')=='ChatGPT':node.set('name','MIRA E4')
  data=E.tostring(root,encoding='utf-8',xml_declaration=True)
 result.append((info,data))
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
 for info,data in result:z.writestr(info,data)
