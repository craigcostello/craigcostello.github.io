document.querySelectorAll('[data-catalog]').forEach(catalog=>{
  const input=catalog.querySelector('input[type=search]');
  const entries=[...catalog.querySelectorAll('.entry')];
  const count=catalog.querySelector('[data-count]');
  const empty=catalog.querySelector('.empty');
  input.addEventListener('input',()=>{
    const query=input.value.trim().toLocaleLowerCase();
    let visible=0;
    entries.forEach(entry=>{entry.hidden=!entry.textContent.toLocaleLowerCase().includes(query);if(!entry.hidden)visible++});
    count.textContent=visible+' of '+entries.length+' entries';
    empty.hidden=visible!==0;
  });
});
function revealHash(){
  const id=decodeURIComponent(location.hash.slice(1));
  if(!id)return;
  const target=document.getElementById(id);
  if(!target)return;
  for(let node=target;node;node=node.parentElement){if(node.tagName==='DETAILS')node.open=true}
  requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
}
window.addEventListener('hashchange',revealHash);
document.querySelectorAll('a[href^="#"]').forEach(link=>{
  link.addEventListener('click',()=>{if(link.hash===location.hash)revealHash()});
});
revealHash();
