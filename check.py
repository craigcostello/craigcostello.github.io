#!/usr/bin/env python3
"""Check the generated site, editorial invariants and retained asset integrity."""
import collections, hashlib, json, pathlib, urllib.parse
from html.parser import HTMLParser
ROOT = pathlib.Path(__file__).resolve().parent

def read(name):
 return json.loads((ROOT/'content'/f'{name}.json').read_text())

class Page(HTMLParser):
 def __init__(self):
  super().__init__(); self.ids=[]; self.urls=[]; self.h1=0; self.headings=[]; self.in_heading=False; self.heading_text=''; self.article_ids=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if attrs.get('id'): self.ids.append(attrs['id'])
  if tag=='article' and attrs.get('id'): self.article_ids.append(attrs['id'])
  if tag=='h1': self.h1+=1
  if tag=='h2': self.in_heading=True; self.heading_text=''
  for key in ['src','href']:
   if attrs.get(key): self.urls.append(attrs[key])
 def handle_endtag(self,tag):
  if tag=='h2': self.in_heading=False; self.headings.append(self.heading_text)
 def handle_data(self,value):
  if self.in_heading: self.heading_text+=value

page=Page(); source=(ROOT/'dist/index.html').read_text(); page.feed(source)
assert page.h1==1, 'Profile must have one primary title'
assert not [key for key,count in collections.Counter(page.ids).items() if count>1], 'Duplicate section IDs'
assert page.headings[:4]==['Watch and listen','In print','Research Publications','Research Talks'], 'Homepage order'
assert all(label in page.headings for label in ['Tutorials','Teaching at QUT','Supervision and mentoring','Service','Experience'])
assert '<nav' not in source and 'zero-knowledge' not in source.lower()
assert 'Cryptography, quantum computers, and the mathematics in between.' not in source
assert 'class="roles interests"' in source, 'Research sentence must use the same profile role typography'
assert read('profile')['linkedin_url'] in source and '>GitHub</a>' not in source
for url in page.urls:
 if url.startswith('/'):
  assert (ROOT/'dist'/urllib.parse.urlsplit(url).path.lstrip('/')).exists(), url
 if url.startswith('#'): assert url[1:] in page.ids, url

media=read('media'); by_id={x['id']:x for x in media}; config=read('site'); branding=read('branding')
assert len(by_id)==len(media), 'Duplicate media IDs'
for item in media:
 expected='print' if item['format']=='article' else 'watch'
 assert item['format'] in ['article','video','podcast','radio'], item['id']
 assert item['category']==expected, 'Mixed media category: '+item['id']
 assert item.get('local_image') or branding.get(item.get('logo_key'),{}).get('available'), 'Missing thumbnail: '+item['id']
for category in ['watch','print']:
 ids=config['featured_'+category]
 assert len(ids)==len(set(ids)), 'Duplicate homepage feature'
 assert all(by_id[id]['category']==category for id in ids), 'Mixed homepage category'
 # Every item appears in its corresponding archive; highlights share the same renderer.
 expected=[x['id'] for x in media if x['category']==category]
 actual=[id for id in page.article_ids if id in expected]
 assert actual==expected, 'Media archive dropped or reordered entries'

papers=read('papers')
assert [id for id in page.article_ids if id.startswith('papers-')]==[p['id'] for p in papers], 'Paper array order must survive the build'
# Keep every migrated paper while allowing Craig to update the editorial order.
original_set=set(read('migration-paper-order')['ids'])
assert original_set.issubset({p['id'] for p in papers}), 'A migrated paper is missing'
for talk in read('talks'):
 assert talk.get('preview_image'), 'Missing slide thumbnail: '+talk['id']
 assert (ROOT/'public'/talk['preview_image'].lstrip('/')).exists(), talk['id']
 assert talk['id'] in page.article_ids, 'Talk missing from archive'

manifest=read('assets'); recorded={x['local_url'] for x in manifest}
actual={'/'+p.relative_to(ROOT/'public').as_posix() for p in (ROOT/'public').rglob('*') if p.is_file() and not any(part.startswith('.') for part in p.relative_to(ROOT/'public').parts)}
assert recorded==actual, 'Asset manifest is stale; run python3 manage.py assets'
for asset in manifest:
 path=ROOT/'dist'/asset['local_url'].lstrip('/')
 assert path.stat().st_size==asset['size_bytes'], str(path)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256'], str(path)

service=read('service')
assert any(p['publication']=='IACR Communications in Cryptology' and p['role']=='Editorial board member' and p['start_year']==2026 and p['end_year'] is None for p in service['editorial'])
assert all('Communications in Cryptology' not in p['conference'] for p in service['committees'])
assert {'EUROCRYPT','CRYPTO'}=={p['conference'] for p in service['committees'] if p['year']==2027}
assert any(p['conference']=='CRYPTO' and p['year']==2025 and p['role']=='Area Chair' for p in service['committees'])
assert all(date in {p['dates'] for p in read('career')} for date in ['2008–2012','2007','2005–2006'])
print(f'Passed: {len(papers)} papers in editorial order, {len(read("talks"))} thumbnail talks, {len(media)} correctly separated media entries, profile/service details and {len(manifest)} asset checksums.')
