"""A compact academic homepage, with media tiles and research before career history."""
def render_home(root,data,preview,a,e,img,archive,target,card):
 profile=data['profile'];branding=data['branding'];media={item['id']:item for item in data['media']};config=data['site']
 def heading(id,title,all_id=None,all_text=None):
  return '<div class="section-heading"><h2 id="'+id+'">'+title+'</h2>'+(a('#'+all_id,all_text) if all_id else '')+'</div>'
 def image(path,alt='',cls='',lazy=True):
  return '<img src="'+img(path)+'" alt="'+e(alt)+'"'+(' class="'+cls+'"' if cls else '')+(' loading="lazy"' if lazy else '')+'>'
 out='<section class="profile" aria-labelledby="name">'+image('/images/craig-costello.jpg','Craig Costello','profile-photo',False)+'<div class="profile-copy"><h1 id="name">Craig Costello</h1><p class="roles">Professor in the School of Computer Science at '+a('https://www.qut.edu.au/','QUT')+'.<br>Chief Investigator in the '+a('https://mathquest.edu.au/','MathQuEST ARC Centre of Excellence')+'.</p><p class="roles interests">I work on post-quantum cryptography and computational number theory.</p><div class="profile-links">'+a('mailto:'+profile['email'],'Email')+a(profile['linkedin_url'],'LinkedIn')+a('#work-with-me','Work with me')+'</div><div class="affiliations">'
 for key,url,label in [('qut','https://www.qut.edu.au/','QUT'),('mathquest','https://mathquest.edu.au/','MathQuEST')]:
  asset=branding.get(key,{})
  if asset.get('available'):out+='<a href="'+url+'">'+image(asset['local_url'],label,'qut-mark' if key=='qut' else '',False)+'</a>'
 out+='</div></div>'+image(branding['quantum_hourglass']['local_url'],'An hourglass with a quantum computer suspended inside','profile-mark',False)+'</section>'
 out+='<section class="section" aria-labelledby="watch"><span id="all-media"></span>'+heading('watch','Watch and listen','all-watch','All audio and video')+'<div class="tile-grid">'
 out+=''.join(card(media[id],'watch') for id in config['featured_watch'])
 out+='</div>'+archive('watch')+'</section>'
 out+='<section class="section" aria-labelledby="in-print">'+heading('in-print','In print','all-print','All written media')+'<div class="press-list">'
 out+=''.join(card(media[id],'print') for id in config['featured_print'])
 out+='</div>'+archive('print')+'</section>'
 out+='<section class="section" aria-labelledby="research-publications">'+heading('research-publications','Research Publications','all-papers','All papers')+'<div class="paper-list">'
 for item in data['papers'][:config['paper_highlight_count']]:
  links=item.get('links',[]);url=target(links[0]) if links else '#research-publications'
  out+='<article class="paper"><div class="paper-year">'+e(item.get('year') or '')+'</div><div><h3>'+a(url,item['title'])+'</h3><p>'+e(item['detail'])+'</p>'
  if len(links)>1:out+='<div class="inline-links">'+''.join(a(target(l),l['text']) for l in links[1:])+'</div>'
  out+='</div></article>'
 out+='</div>'+archive('papers')+'</section>'
 out+='<section class="section" aria-labelledby="research-talks">'+heading('research-talks','Research Talks','all-talks','All research talks')+'<div class="tile-grid">'
 out+=''.join(card(item,'talks') for item in data['talks'][:config['talk_highlight_count']])
 out+='</div>'+archive('talks')+'</section>'
 out+='<section class="section" aria-labelledby="tutorials">'+heading('tutorials','Tutorials')+'<div class="tutorial-grid">'
 for item in data['tutorials']:
  url=target(item['links'][0]);thumb_class='slide-preview' if item['id']=='tutorials-001' else ''
  out+='<article class="tutorial"><div><a class="tutorial-preview" href="'+e(url)+'">'+image(item['preview_image'],item['preview_caption'],thumb_class)+'</a><p class="tutorial-caption">'+e(item['preview_caption'])+'</p></div><div><h3>'+a(url,item['title'])+'</h3><p>'+e(item['description'])+'</p><div class="inline-links">'
  out+=a(url,'Tutorial · PDF')
  for link in item['links'][1:]:out+=a(target(link),link['text'])
  out+='</div></div></article>'
 out+='</div><p class="historical-note">The isogeny tutorial is a historical introduction to SIDH, which is no longer secure.</p></section>'
 out+='<section class="section" aria-labelledby="teaching">'+heading('teaching','Teaching at QUT')+'<p class="teaching-copy">I teach algorithms, cryptography and cybersecurity, connecting mathematical ideas with the systems people use every day.</p><div class="course"><div class="course-code">CAB340</div><p><strong>Cryptography</strong><br>Unit Coordinator and Lecturer. Intuition before mathematics; examples before definitions.</p></div><div class="course"><div class="course-code">CAB301</div><p><strong>Algorithms and Complexity</strong><br>Lecturer.</p></div><div class="course"><div class="course-code">IFB240</div><p><strong>Cyber Security</strong><br>Lecturer.</p></div></section>'
 people=data['people']
 out+='<section class="section" aria-labelledby="supervision">'+heading('supervision','Supervision and mentoring')+'<div class="people-grid">'
 for key,title in [('current','Current supervision · QUT'),('former','Previous PhD co-supervision')]:
  out+='<div><h3>'+title+'</h3><ul class="people-list">'
  for person in people[key]:
   name=a(person['url'],person['name']) if person.get('url') else e(person['name'])
   out+='<li class="person"><div class="person-name">'+name+'</div><div class="person-detail">'+e(person['role'])+(' · '+e(person['institution']) if key=='former' else '')+'</div></li>'
  out+='</ul></div>'
 out+='</div><details class="archive" id="microsoft-interns"><summary>Microsoft Research interns</summary><div class="archive-body"><p class="intern-intro">Summer research projects I supervised at Microsoft. Institutions shown are those at the time of the internship.</p><ul class="intern-list">'
 for person in people['interns']:
  name=a(person['url'],person['name']) if person.get('url') else e(person['name'])
  out+='<li><div class="intern-name">'+name+'</div><div class="intern-detail">'+e(person['years'])+' · '+e(person['institution'])+'</div></li>'
 out+='</ul></div></details></section>'
 service=data['service']
 out+='<section class="section" aria-labelledby="service">'+heading('service','Service')+'<div class="service-leadership">'
 for role in service['leadership']:
  title=role['conference']+' '+str(role['year'])
  out+='<p>'+a(role['url'],title)+' · '+e(role['role'])+'</p>'
 out+='</div>'
 for role in service.get('editorial',[]):
  dates=str(role['start_year'])+'–'+(str(role['end_year']) if role.get('end_year') else 'ongoing')
  out+='<p class="editorial-service">'+a(role['url'],role['publication'])+' · '+e(role['role'])+' ('+e(dates)+')</p>'
 out+='<p class="service-label">Program committees</p><div class="service-years">'
 years=sorted({p['year'] for p in service['committees'] if p.get('year')},reverse=True)
 for year in years[:3]:
  entries=[p for p in service['committees'] if p.get('year')==year]
  out+='<div class="service-year"><span>'+str(year)+'</span><p>'+e(' · '.join(p['conference']+(' (Area Chair)' if p['role']=='Area Chair' else '') for p in entries))+'</p></div>'
 out+='</div><details class="archive" id="earlier-service"><summary>Earlier program committees</summary><div class="archive-body service-years">'
 for year in years[3:]:
  entries=[p for p in service['committees'] if p.get('year')==year]
  out+='<div class="service-year"><span>'+str(year)+'</span><p>'+e(' · '.join(p['conference'] for p in entries))+'</p></div>'
 out+='</div></details>'
 for committee in service['committees']:
  if committee['year'] is None:out+='<p class="other-service">'+e(committee['conference'])+'</p>'
 out+='</section>'
 out+='<section class="opportunities" aria-labelledby="work-with-me"><h2 id="work-with-me">Let’s work on hard problems.</h2><p>Interested in a PhD, Masters or Honours project with me at QUT?</p><p>Please get in touch only if your existing studies or research demonstrate a relevant background in mathematics, computer science or cryptography, together with a clear interest in my research areas.</p><p>'+a('mailto:'+profile['email']+'?subject=Research%20supervision%20enquiry','Get in touch')+'</p><p class="topic-list">Post-quantum cryptography · Computational number theory · Quantum algorithms</p></section>'
 out+='<section class="section career-section" aria-labelledby="experience">'+heading('experience','Experience')+'<div class="career-list">'
 for job in data['career']:
  out+='<article class="career-item"><div class="career-date">'+e(job['dates'])+'</div><div class="career-content"><h3>'+a(job['url'],job['organisation'])+'</h3><p>'+e(job['role'])+'<br>'+e(job['location'])+'</p>'
  if job.get('detail'):out+='<details><summary>Roles at Microsoft Research</summary><p>'+e(job['detail'])+'</p></details>'
  out+='</div></article>'
 return out+'</div></section>'
