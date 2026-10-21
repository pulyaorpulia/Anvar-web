document.addEventListener('DOMContentLoaded', function () {

    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar--scrolled');
            } else {
                navbar.classList.remove('navbar--scrolled');
            }
        });
    }

    const burgerBtn = document.getElementById('burgerBtn');
    const navMenu = document.getElementById('navMenu');
    if (burgerBtn && navMenu) {
        burgerBtn.addEventListener('click', function () {
            burgerBtn.classList.toggle('active');
            navMenu.classList.toggle('open');
        });
    }

    const messages = document.querySelectorAll('.message');
    messages.forEach(function (msg) {
        setTimeout(function () {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s ease';
            setTimeout(function () { msg.remove(); }, 500);
        }, 3000);
    });

});

// ACHIEVEMENTS ANIMATION
function animateCount(el) {
    const target = parseInt(el.getAttribute('data-target'));
    const duration = 1800;
    const step = target / (duration / 16);
    let current = 0;

    const timer = setInterval(function () {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        el.textContent = Math.floor(current);
    }, 16);
}

function animateCircle(circle) {
    const percent = parseFloat(circle.getAttribute('data-percent'));
    const circumference = 2 * Math.PI * 35;
    const offset = circumference - (percent / 100) * circumference;
    setTimeout(function () {
        circle.style.strokeDashoffset = offset;
    }, 200);
}

const achievementObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
        if (entry.isIntersecting) {
            const item = entry.target;
            const delay = parseInt(item.getAttribute('data-delay')) || 0;

            setTimeout(function () {
                item.classList.add('visible');

                const counter = item.querySelector('.count');
                if (counter) animateCount(counter);

                const circle = item.querySelector('.achievement__circle-fill');
                if (circle) animateCircle(circle);
            }, delay);

            achievementObserver.unobserve(item);
        }
    });
}, { threshold: 0.3 });

document.querySelectorAll('.achievement__item').forEach(function (item) {
    achievementObserver.observe(item);
});

// SERVICES ANIMATION
const serviceObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
        if (entry.isIntersecting) {
            const row = entry.target;
            const index = parseInt(row.getAttribute('data-index')) || 1;
            setTimeout(function () {
                row.classList.add('visible');
            }, index * 80);
            serviceObserver.unobserve(row);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.service__row').forEach(function (row) {
    serviceObserver.observe(row);
});

// TEAM SLIDER
(function () {
    const cards = document.querySelectorAll('.team__card');
    const dotsWrap = document.getElementById('teamDots');
    const prevBtn = document.getElementById('teamPrev');
    const nextBtn = document.getElementById('teamNext');
    const grid = document.getElementById('teamGrid');

    if (!cards.length || !dotsWrap || !prevBtn || !nextBtn || !grid) return;

    // Telefonda 2 ta, kompyuterda 3 ta
    const VISIBLE = window.innerWidth <= 768 ? 2 : 3;
    const total = cards.length;
    const pages = Math.ceil(total / VISIBLE);
    let current = 0;

    // Nuqtalar (har sahifaga bitta)
    for (let i = 0; i < pages; i++) {
        const dot = document.createElement('button');
        dot.className = 'team__dot';
        dot.setAttribute('aria-label', (i + 1) + '-sahifa');
        dot.addEventListener('click', function () { show(i); });
        dotsWrap.appendChild(dot);
    }
    const dots = dotsWrap.querySelectorAll('.team__dot');

    function show(page) {
        current = Math.max(0, Math.min(page, pages - 1));
        const start = current * VISIBLE;
        const end = start + VISIBLE;

        cards.forEach(function (card, i) {
            const inPage = i >= start && i < end;
            card.classList.remove('visible');
            card.classList.toggle('active', inPage);
            if (inPage) {
                const delay = (i - start) * 100;
                setTimeout(function () {
                    card.classList.add('visible');
                }, 30 + delay);
            }
        });

        dots.forEach(function (d, i) {
            d.classList.toggle('active', i === current);
        });
        prevBtn.disabled = current === 0;
        nextBtn.disabled = current === pages - 1;
    }

    prevBtn.addEventListener('click', function () { show(current - 1); });
    nextBtn.addEventListener('click', function () { show(current + 1); });

    // Auto slide — har 7 soniyada
    setInterval(function () {
        show(current + 1 >= pages ? 0 : current + 1);
    }, 7000);

    // Telefonda barmoq bilan surish (swipe)
    let startX = 0;
    grid.addEventListener('touchstart', function (e) {
        startX = e.touches[0].clientX;
    }, { passive: true });
    grid.addEventListener('touchend', function (e) {
        const diff = e.changedTouches[0].clientX - startX;
        if (Math.abs(diff) > 50) show(diff < 0 ? current + 1 : current - 1);
    }, { passive: true });

    show(0);
})();


// CTA VIDEO
const ctaPreview = document.getElementById('ctaPreview');
const ctaVideo = document.getElementById('ctaVideo');
const ctaControls = document.getElementById('ctaControls');

if (ctaPreview && ctaVideo) {
    ctaPreview.addEventListener('click', function () {
        ctaPreview.style.display = 'none';
        ctaVideo.style.display = 'block';
        ctaControls.style.display = 'flex';
        ctaVideo.play();
    });
}

// LIGHTBOX
const lbSources = document.querySelectorAll('.lightbox-sources img');
const lbTriggers = document.querySelectorAll('.lightbox-trigger');
let lbIndex = 0;

if (lbSources.length && lbTriggers.length) {
    const lb = document.createElement('div');
    lb.className = 'main-lightbox';
    lb.innerHTML = `
        <button class="main-lightbox__close">✕</button>
        <button class="main-lightbox__prev">‹</button>
        <button class="main-lightbox__next">›</button>
        <div class="main-lightbox__counter"></div>
        <div class="main-lightbox__container">
            <img class="main-lightbox__img" src="" alt="">
        </div>
    `;
    document.body.appendChild(lb);

    function lbShow(index) {
        lbIndex = index;
        lb.querySelector('.main-lightbox__img').src = lbSources[lbIndex].src;
        lb.querySelector('.main-lightbox__counter').textContent = (lbIndex + 1) + ' / ' + lbSources.length;
        lb.querySelector('.main-lightbox__prev').disabled = lbIndex === 0;
        lb.querySelector('.main-lightbox__next').disabled = lbIndex === lbSources.length - 1;
        lb.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function lbClose() {
        lb.classList.remove('active');
        document.body.style.overflow = '';
    }

    lbTriggers.forEach(function(el) {
        el.style.cursor = 'zoom-in';
        el.addEventListener('click', function() {
            lbShow(parseInt(el.getAttribute('data-index')) || 0);
        });
    });

    lb.querySelector('.main-lightbox__close').addEventListener('click', lbClose);
    lb.querySelector('.main-lightbox__prev').addEventListener('click', function() { if (lbIndex > 0) lbShow(lbIndex - 1); });
    lb.querySelector('.main-lightbox__next').addEventListener('click', function() { if (lbIndex < lbSources.length - 1) lbShow(lbIndex + 1); });
    lb.addEventListener('click', function(e) { if (e.target === this) lbClose(); });

    document.addEventListener('keydown', function(e) {
        if (!lb.classList.contains('active')) return;
        if (e.key === 'Escape') lbClose();
        if (e.key === 'ArrowLeft' && lbIndex > 0) lbShow(lbIndex - 1);
        if (e.key === 'ArrowRight' && lbIndex < lbSources.length - 1) lbShow(lbIndex + 1);
    });
}