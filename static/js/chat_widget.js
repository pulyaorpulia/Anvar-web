(function(){
  var btn=document.getElementById('aa-chat-btn'), tip=document.getElementById('aa-chat-tip'),
      box=document.getElementById('aa-chat-box'), msgs=document.getElementById('aa-msgs'),
      input=document.getElementById('aa-input'), send=document.getElementById('aa-send');
  if(!btn||!box) return;

  var API=box.dataset.api||'/api/chat/', TOKEN=box.dataset.csrf||'';
  var chatHistory=[], busy=false, MAX_HISTORY=20;

  function getCsrf(){
    var m=document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : TOKEN;
  }

  function add(text, who){
    var d=document.createElement('div'); d.className='aa-m '+who; d.textContent=text;
    msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight; return d;
  }
  function openBox(){
    box.classList.add('open'); tip.style.display='none'; btn.setAttribute('aria-expanded','true'); input.focus();
    if(!msgs.children.length) add("Salom! Men Aanick sun'iy intellektman. Qanday yordam bera olaman?", 'bot');
  }
  function closeBox(){ box.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }
  function toggle(){ box.classList.contains('open') ? closeBox() : openBox(); }

  btn.addEventListener('click', toggle);
  tip.addEventListener('click', openBox);
  document.getElementById('aa-close').addEventListener('click', closeBox);
  document.addEventListener('keydown', function(e){ if(e.key==='Escape' && box.classList.contains('open')) closeBox(); });

  async function submit(){
    var text=input.value.trim(); if(!text||busy) return;
    input.value=''; add(text,'me');
    chatHistory.push({role:'user',content:text});
    if(chatHistory.length>MAX_HISTORY) chatHistory=chatHistory.slice(-MAX_HISTORY);
    busy=true; send.disabled=true;
    var wait=add('...','bot');
    try{
      var r=await fetch(API,{method:'POST',credentials:'same-origin',
        headers:{'Content-Type':'application/json','X-CSRFToken':getCsrf()},
        body:JSON.stringify({messages:chatHistory})});
      var j=await r.json().catch(function(){ return {}; });
      if(!r.ok || !j.reply) throw new Error('bad response');
      wait.textContent=j.reply;
      chatHistory.push({role:'assistant',content:j.reply});
    }catch(e){
      wait.textContent="Aloqa xatosi. Qayta urinib ko'ring.";
      chatHistory.pop();
    }
    busy=false; send.disabled=false; msgs.scrollTop=msgs.scrollHeight; input.focus();
  }
  send.addEventListener('click', submit);
  input.addEventListener('keydown', function(e){
    if(e.key==='Enter' && !e.shiftKey && !e.isComposing){ e.preventDefault(); submit(); }
  });
})();