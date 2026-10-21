(function () {
    const root = document.getElementById('aichat');
    if (!root) return;

    const url = root.dataset.url;
    const csrf = root.dataset.csrf;
    const fab = document.getElementById('aichatFab');
    const bubble = document.getElementById('aichatBubble');
    const win = document.getElementById('aichatWindow');
    const closeBtn = document.getElementById('aichatClose');
    const box = document.getElementById('aichatMessages');
    const form = document.getElementById('aichatForm');
    const input = document.getElementById('aichatInput');
    const sendBtn = form.querySelector('button');

    const history = [];

    function addMsg(text, who, extra) {
        const el = document.createElement('div');
        el.className = 'aichat__msg aichat__msg--' + who + (extra ? ' ' + extra : '');
        el.textContent = text;
        box.appendChild(el);
        box.scrollTop = box.scrollHeight;
        return el;
    }

    function open() {
        win.hidden = false;
        bubble.classList.add('hide');
        if (!box.children.length) {
            addMsg("Salom! Men Aanick sun'iy intellektman. Logotip, brending yoki boshqa dizayn xizmatlari bo'yicha qanday yordam bera olaman?", 'bot');
        }
        input.focus();
    }

    function close() { win.hidden = true; }

    fab.addEventListener('click', function () { win.hidden ? open() : close(); });
    closeBtn.addEventListener('click', close);

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;

        addMsg(text, 'user');
        history.push({ role: 'user', content: text });
        input.value = '';
        sendBtn.disabled = true;
        const typing = addMsg('Yozmoqda...', 'bot', 'aichat__msg--typing');

        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
                body: JSON.stringify({ messages: history })
            });
            const data = await res.json();
            typing.remove();
            addMsg(data.reply, 'bot');
            if (res.ok) history.push({ role: 'assistant', content: data.reply });
        } catch (err) {
            typing.remove();
            addMsg("Aloqa xatosi. Qayta urinib ko'ring.", 'bot');
        } finally {
            sendBtn.disabled = false;
            input.focus();
        }
    });
})();