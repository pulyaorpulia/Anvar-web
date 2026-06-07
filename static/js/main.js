document.addEventListener('DOMContentLoaded', function () {

    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar--scrolled');
        } else {
            navbar.classList.remove('navbar--scrolled');
        }
    });

    const burgerBtn = document.getElementById('burgerBtn');
    const navMenu = document.getElementById('navMenu');
    burgerBtn.addEventListener('click', function () {
        burgerBtn.classList.toggle('active');
        navMenu.classList.toggle('open');
    });


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

    if (!cards.length) return;

    const VISIBLE = window.innerWidth <= 480 ? 1 : window.innerWidth <= 768 ? 2 : 3;
    const total = cards.length;
    let current = 0;

    // Dotlar yaratish
    const pageCount = Math.ceil(total / VISIBLE);
    for (let i = 0; i < pageCount; i++) {
        const dot = document.createElement('button');
        dot.className = 'team__dot' + (i === 0 ? ' active' : '');
        dot.setAttribute('aria-label', i + 1 + '-sahifa');
        dot.addEventListener('click', function () { goTo(i); });
        dotsWrap.appendChild(dot);
    }

    function showCards(page) {
        const start = page * VISIBLE;
        const end = start + VISIBLE;

        cards.forEach(function (card, i) {
            card.classList.remove('active', 'visible');
            if (i >= start && i < end) {
                card.classList.add('active');
                setTimeout(function () {
                    card.classList.add('visible');
                }, (i - start) * 100);
            }
        });

        // Dotlar
        document.querySelectorAll('.team__dot').forEach(function (dot, i) {
            dot.classList.toggle('active', i === page);
        });

        // Tugmalar
        prevBtn.disabled = page === 0;
        nextBtn.disabled = page >= pageCount - 1;
        current = page;
    }

    function goTo(page) {
        if (page < 0 || page >= pageCount) return;
        showCards(page);
    }

    prevBtn.addEventListener('click', function () { goTo(current - 1); });
    nextBtn.addEventListener('click', function () { goTo(current + 1); });

    // Auto slide — har 4 soniyada
    setInterval(function () {
        const next = current + 1 >= pageCount ? 0 : current + 1;
        goTo(next);
    }, 7000);

    // Boshlash
    showCards(0);

    // Scroll animatsiya
    const teamObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                document.querySelectorAll('.team__card.active').forEach(function (card, i) {
                    setTimeout(function () {
                        card.classList.add('visible');
                    }, i * 120);
                });
                teamObserver.disconnect();
            }
        });
    }, { threshold: 0.2 });

    const teamSection = document.querySelector('.team');
    if (teamSection) teamObserver.observe(teamSection);
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


