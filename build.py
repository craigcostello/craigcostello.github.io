#!/usr/bin/env python3
"""Build the single-page academic site and legacy routes. Standard library only."""
import base64,html,json,mimetypes,pathlib,shutil,urllib.parse
from homepage import render_home
from cards import render_card
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'dist'
DATA={key:json.loads((ROOT/'content'/f'{key}.json').read_text()) for key in ['papers','talks','media','tutorials','profile','people','career','site','branding','service']}
# Array order is editorial: it matches the live page and puts new additions first.
DATA['watch']=[item for item in DATA['media'] if item['category']=='watch']
DATA['print']=[item for item in DATA['media'] if item['category']=='print']
CSS=(ROOT/'src/styles.css').read_text()
JS=(ROOT/'src/site.js').read_text()
def esc(value):return html.escape(str(value),quote=True)
def href(url,text,cls=''):
 return '<a href="'+esc(url)+'"'+(' class="'+cls+'"' if cls else '')+'>'+esc(text)+'</a>'
def target(item,preview=False):
 return item['original_url'] if preview else item.get('local_url',item['original_url'])
def image_url(url,preview=False):
 if not preview:return url
 path=ROOT/'public'/url.lstrip('/')
 mime=mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
 return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
def card(item,name,preview=False,is_archive=False):
 return render_card(item,name,a=href,e=esc,img=lambda u:image_url(u,preview),target=lambda l:target(l,preview),branding=DATA['branding'],archive=is_archive)
def archive(name,preview=False):
 labels={'watch':'All podcasts, interviews and videos','print':'All written media','papers':'All papers','talks':'All research talks'}
 label=labels[name];items=DATA[name]
 out='<details class="archive" id="all-'+name+'"><summary>'+label+' <span>('+str(len(items))+')</span></summary><div class="archive-body" data-catalog><div class="toolbar"><label><span class="sr-only">Search '+esc(label.lower())+'</span><input type="search" aria-label="Search '+esc(label.lower())+'" placeholder="Search titles, venues or names…"></label><span class="count" data-count aria-live="polite">'+str(len(items))+' entries</span></div><p class="empty" hidden>No matching entries. Try another search.</p>'
 if name in ['watch','print','talks']:
  out+='<div class="'+('press-list' if name=='print' else 'tile-grid')+'">'
  out+=''.join(card(item,name,preview,True) for item in items)
  return out+'</div></div></details>'
 for item in items:
  links=item.get('links',[]);title=href(target(links[0],preview),item['title']) if links else esc(item['title'])
  out+='<article class="entry" id="'+esc(item['id'])+'"><h3>'+title+'</h3><p class="detail">'+esc(item['detail'])+'</p><div class="links">'
  seen=set()
  for i,link in enumerate(links):
   url=target(link,preview)
   if url in seen:continue
   seen.add(url)
   kind=link.get('asset_type')
   text='Slides · PDF' if kind=='PDF' and name=='talks' else 'Paper' if i==0 and name=='papers' else 'Watch / listen' if i==0 and name=='media' else link['text']
   if len(text)>45:text='Source'
   out+=href(url,text)
  out+='</div></article>'
 return out+'</div></details>'
def document(body):
 icon='data:image/svg+xml,'+urllib.parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" fill="#1772d0"/><text x="20" y="28" text-anchor="middle" fill="white" font-family="Arial" font-size="25">C</text></svg>')
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Craig Costello · Cryptography &amp; computational number theory</title><meta name="description" content="Professor at QUT and Chief Investigator in MathQuEST. Post-quantum cryptography and computational number theory, talks, research and teaching."><link rel="icon" href="'+icon+'"><style>'+CSS+'</style></head><body><a class="skip" href="#main">Skip to content</a><main id="main" class="wrap">'+body+'</main><footer class="wrap footer"><div class="footer-inner"><p>Post-quantum cryptography &amp; computational number theory</p><p>'+href('mailto:'+DATA['profile']['email'],DATA['profile']['email'])+' · '+href('#name','Back to top')+'</p></div></footer><script>'+JS+'</script></body></html>'
def make(preview=False):
 return document(render_home(ROOT,DATA,preview,href,esc,lambda u:image_url(u,preview),lambda n:archive(n,preview),lambda l:target(l,preview),lambda item,kind:card(item,kind,preview)))
if OUT.exists():shutil.rmtree(OUT)
shutil.copytree(ROOT/'public',OUT,ignore=lambda directory,names:[name for name in names if name.startswith('.')])
(OUT/'index.html').write_text(make(),encoding='utf-8')
(OUT/'.nojekyll').touch()
for old,new in {'home':'#name','papers':'#all-papers','talks':'#all-talks','media':'#watch','tutorials':'#tutorials'}.items():
 path=OUT/old/'index.html';path.parent.mkdir(exist_ok=True)
 path.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Craig Costello</title><meta http-equiv="refresh" content="0;url=/'+new+'"><a href="/'+new+'">Continue to Craig Costello’s website</a></html>')
(OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Page not found · Craig Costello</title><main><h1>Page not found</h1><p>'+href('/','Return to Craig Costello’s homepage')+'</p></main></html>')
(ROOT.parent/'Craig-Costello-Website-Preview.html').write_text(make(True),encoding='utf-8')
print('Built single-page site, searchable in-page archives, legacy routes and standalone preview.')
