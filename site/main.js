/* =========================================================
   ATELIER template — interactions
   No dependencies. Everything degrades gracefully.
   ========================================================= */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(pointer: fine)').matches;
  const lerp = (a, b, n) => a + (b - a) * n;

  /* ---------- 1. Custom cursor (desktop, non-reduced only) ---------- */
  if (finePointer && !reduced) {
    document.body.classList.add('has-cursor');
    const ring = document.querySelector('.cursor__ring');
    const dot  = document.querySelector('.cursor__dot');
    let mx = innerWidth / 2, my = innerHeight / 2;   // mouse
    let rx = mx, ry = my;                            // ring (trails)

    addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate(${mx}px, ${my}px) translate(-50%,-50%)`;
    });
    (function raf() {
      rx = lerp(rx, mx, 0.18); ry = lerp(ry, my, 0.18);
      ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%,-50%)`;
      requestAnimationFrame(raf);
    })();

    // grow ring over interactive things
    document.querySelectorAll('[data-cursor-hover], a, button, input').forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
    });
  }

  /* ---------- 2. Header stuck + scroll progress ---------- */
  const header = document.querySelector('[data-header]');
  const progress = document.querySelector('[data-progress]');
  const onScroll = () => {
    const y = scrollY;
    header.classList.toggle('is-stuck', y > 20);
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- 3. Reveal on scroll ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));

  /* ---------- 4. Parallax (rAF, throttled to scroll) ---------- */
  if (!reduced) {
    const items = [...document.querySelectorAll('[data-parallax]')];
    let ticking = false;
    const move = () => {
      const vh = innerHeight;
      items.forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        const speed = parseFloat(el.dataset.parallax) || 0.15;
        const offset = (r.top + r.height / 2 - vh / 2) * -speed;
        el.style.transform = `translateY(${offset.toFixed(1)}px)`;
      });
      ticking = false;
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(move); } }, { passive: true });
    move();
  }

  /* ---------- 5. Fading transform carousels (hero + quotes) ---------- */
  document.querySelectorAll('[data-carousel]').forEach(car => {
    const track = car.querySelector('[data-track]');
    const dotsBox = car.querySelector('[data-dots]');
    const slides = track.children;
    const count = slides.length;
    let i = 0, timer;
    const interval = parseInt(car.dataset.autoplay) || 0;

    // build dots
    const dots = [...slides].map((_, n) => {
      const b = document.createElement('button');
      b.className = 'dot'; b.setAttribute('aria-label', `Go to slide ${n + 1}`);
      b.addEventListener('click', () => { go(n); restart(); });
      dotsBox.appendChild(b);
      return b;
    });

    const go = (n) => {
      i = (n + count) % count;
      track.style.transform = `translateX(${-i * 100}%)`;
      dots.forEach((d, k) => d.classList.toggle('is-active', k === i));
    };
    const restart = () => {
      if (!interval || reduced) return;
      clearInterval(timer);
      timer = setInterval(() => go(i + 1), interval);
    };

    go(0); restart();
    car.addEventListener('mouseenter', () => clearInterval(timer));
    car.addEventListener('mouseleave', restart);
  });

  /* ---------- 6. Products drag-carousel arrows ---------- */
  const featured = document.getElementById('featured');
  if (featured) {
    const scroller = featured.querySelector('[data-drag-carousel]');
    const step = () => (scroller.querySelector('.product')?.offsetWidth || 320) + 24;
    featured.querySelector('[data-prev]')?.addEventListener('click', () => scroller.scrollBy({ left: -step(), behavior: 'smooth' }));
    featured.querySelector('[data-next]')?.addEventListener('click', () => scroller.scrollBy({ left:  step(), behavior: 'smooth' }));

    // click-drag to scroll (desktop nicety; touch already scrolls natively)
    let down = false, startX, startL;
    scroller.addEventListener('mousedown', e => { down = true; startX = e.pageX; startL = scroller.scrollLeft; scroller.style.cursor = 'grabbing'; });
    addEventListener('mouseup', () => { down = false; scroller.style.cursor = ''; });
    scroller.addEventListener('mousemove', e => { if (down) { e.preventDefault(); scroller.scrollLeft = startL - (e.pageX - startX); } });
  }

  /* ---------- 7. Count-up stats ---------- */
  const counters = document.querySelectorAll('[data-count]');
  const cio = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target, target = parseInt(el.dataset.count);
      if (reduced) { el.textContent = target; cio.unobserve(el); return; }
      let n = 0; const t0 = performance.now(), dur = 1200;
      const tick = (t) => {
        const p = Math.min((t - t0) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      cio.unobserve(el);
    });
  }, { threshold: 0.6 });
  counters.forEach(c => cio.observe(c));

  /* ---------- 8. Mobile menu ---------- */
  const burger = document.querySelector('[data-burger]');
  const nav = document.querySelector('[data-nav]');
  burger?.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open);
  });
  nav?.querySelectorAll('.nav__link').forEach(l => l.addEventListener('click', () => {
    nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false');
  }));
})();
