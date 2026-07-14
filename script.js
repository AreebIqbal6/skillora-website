/* ============================================
   SKILLORA — GSAP Motion System
   Lenis + GSAP ScrollTrigger + custom cursor
   ============================================ */

window.addEventListener('load', function () {
  'use strict';

  // ============ THEME TOGGLE ============
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      document.documentElement.classList.toggle('light-mode');
      const isLight = document.documentElement.classList.contains('light-mode');
      localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
  }

  // ============ LENIS SMOOTH SCROLL ============
  let lenis;
  try {
    lenis = new Lenis({ duration: 1.2, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothTouch: false });
    function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    // Sync GSAP ScrollTrigger with Lenis
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  } catch (e) { /* fallback: native scroll */ }

  // ============ CUSTOM CURSOR ============
  const cur = document.getElementById('cur');
  if (cur && window.innerWidth > 1024) {
    let mx = 0, my = 0, cx = 0, cy = 0;
    window.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    gsap.ticker.add(() => {
      cx += (mx - cx) * 0.12;
      cy += (my - cy) * 0.12;
      gsap.set(cur, { x: cx, y: cy });
    });
    document.querySelectorAll('[data-hover], a, button').forEach(el => {
      el.addEventListener('mouseenter', () => cur.classList.add('is-hover'));
      el.addEventListener('mouseleave', () => cur.classList.remove('is-hover'));
    });
  } else if (cur) { cur.style.display = 'none'; }

  // ============ HERO ENTRANCE — orchestrated timeline ============
  const heroTL = gsap.timeline({ delay: 0.2, defaults: { ease: 'expo.out' } });

  // Nav slides in
  heroTL.from('.nav', { y: -40, opacity: 0, duration: 1 }, 0);

  // Eyebrow fades
  heroTL.from('.hero-eyebrow', { y: 20, opacity: 0, duration: 0.8 }, 0.3);

  // Hero lines slide up individually — the key Framer effect
  document.querySelectorAll('.hero-line span').forEach((span, i) => {
    gsap.set(span, { y: '110%' });
    heroTL.to(span, { y: '0%', duration: 1.2, ease: 'expo.out' }, 0.35 + i * 0.12);
  });

  // Hero bottom row
  heroTL.from('.hero-row', { y: 40, opacity: 0, duration: 1 }, 0.9);

  // Hero stroke text fills blue after entrance
  heroTL.to('.hero .t-stroke', {
    '-webkit-text-fill-color': '#0055FF',
    duration: 0.8, ease: 'power2.inOut'
  }, 1.4);

  // ============ SCROLL-TRIGGERED SECTIONS ============
  gsap.registerPlugin(ScrollTrigger);

  // Generic fade-up for [data-gsap="fade"]
  document.querySelectorAll('[data-gsap="fade"]').forEach(el => {
    gsap.from(el, {
      y: 60, opacity: 0, duration: 1, ease: 'expo.out',
      scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none none' }
    });
  });

  // Staggered children for [data-gsap="stagger"] (bento, testimonials)
  document.querySelectorAll('[data-gsap="stagger"]').forEach(parent => {
    const kids = parent.children;
    gsap.from(kids, {
      y: 50, opacity: 0, duration: 0.9, ease: 'expo.out',
      stagger: 0.1,
      scrollTrigger: { trigger: parent, start: 'top 82%', toggleActions: 'play none none none' }
    });
  });

  // .dim text → Skillora blue on scroll
  document.querySelectorAll('.dim').forEach(el => {
    gsap.to(el, {
      color: '#0055FF', duration: 0.8, ease: 'power2.inOut',
      scrollTrigger: { trigger: el, start: 'top 80%', toggleActions: 'play none none none' }
    });
  });

  // .t-stroke outside hero → fill blue on scroll
  document.querySelectorAll('.t-stroke').forEach(el => {
    if (el.closest('.hero')) return; // hero handled above
    gsap.to(el, {
      '-webkit-text-fill-color': '#0055FF', duration: 0.8, ease: 'power2.inOut',
      scrollTrigger: { trigger: el, start: 'top 80%', toggleActions: 'play none none none' }
    });
  });

  // Process items — slide in one by one
  document.querySelectorAll('[data-gsap="stagger-lines"]').forEach(parent => {
    const items = parent.children;
    gsap.from(items, {
      x: -30, opacity: 0, duration: 0.8, ease: 'expo.out',
      stagger: 0.12,
      scrollTrigger: { trigger: parent, start: 'top 80%', toggleActions: 'play none none none' }
    });
  });

  // Work cards — scale in from scroll
  document.querySelectorAll('.w-card').forEach((card, i) => {
    gsap.from(card, {
      scale: 0.9, opacity: 0, duration: 0.8, ease: 'expo.out',
      delay: i * 0.08,
      scrollTrigger: { trigger: card, start: 'top 90%', toggleActions: 'play none none none' }
    });
  });

  // ============ PARALLAX ============
  // Section tags get subtle parallax
  document.querySelectorAll('.sec-tag').forEach(tag => {
    gsap.to(tag, {
      y: -20,
      scrollTrigger: { trigger: tag, start: 'top bottom', end: 'bottom top', scrub: 1 }
    });
  });

  // Ticker parallax speed shift
  const tickTrack = document.querySelector('.tick-track');
  if (tickTrack) {
    gsap.to(tickTrack, {
      x: -60,
      scrollTrigger: { trigger: '.tick', start: 'top bottom', end: 'bottom top', scrub: 2 }
    });
  }

  // ============ COUNTERS ============
  let countersDone = false;
  const mGrid = document.querySelector('.m-grid');
  if (mGrid) {
    ScrollTrigger.create({
      trigger: mGrid, start: 'top 80%',
      onEnter: () => {
        if (countersDone) return;
        countersDone = true;
        document.querySelectorAll('.counter').forEach((el, i) => {
          const target = +el.dataset.target;
          gsap.to({ val: 0 }, {
            val: target, duration: 2, ease: 'expo.out', delay: i * 0.15,
            onUpdate: function () { el.textContent = Math.round(this.targets()[0].val); }
          });
        });
      }
    });
  }

  // ============ FAQ ============
  document.querySelectorAll('.faq-item').forEach(item => {
    const btn = item.querySelector('.faq-q');
    const ans = item.querySelector('.faq-a');
    const inner = item.querySelector('.faq-a-text');

    if (item.classList.contains('on') && inner) {
      ans.style.maxHeight = inner.scrollHeight + 28 + 'px';
    }

    btn.addEventListener('click', () => {
      const wasOn = item.classList.contains('on');
      document.querySelectorAll('.faq-item').forEach(o => {
        o.classList.remove('on');
        o.querySelector('.faq-a').style.maxHeight = '0';
      });
      if (!wasOn) {
        item.classList.add('on');
        ans.style.maxHeight = inner.scrollHeight + 28 + 'px';
      }
    });
  });

  // ============ MOBILE MENU SETUP ============
  const navToggle = document.getElementById('navToggle');
  const navMid = document.getElementById('navMid'); // Correct ID!
  
  if (navToggle && navMid) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('on');
      navMid.classList.toggle('open');
      document.body.style.overflow = navMid.classList.contains('open') ? 'hidden' : '';
    });
    
    // Close menu when a link is clicked
    navMid.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      navToggle.classList.remove('on'); 
      navMid.classList.remove('open'); 
      document.body.style.overflow = '';
    }));
  }

  // Mobile Dropdown Frost Fix: Move nav-mid outside of nav-pill on mobile so backdrop-filter works!
  function handleNavReparent() {
    const navWrap = document.querySelector('.nav .wrap');
    const navPill = document.querySelector('.nav-pill');
    if (!navWrap || !navPill || !navMid) return;

    if (window.innerWidth <= 768) {
      if (navMid.parentElement !== navWrap) navWrap.appendChild(navMid);
    } else {
      const themeToggle = document.querySelector('.theme-toggle');
      if (navMid.parentElement !== navPill) {
        if (themeToggle) navPill.insertBefore(navMid, themeToggle);
        else navPill.appendChild(navMid);
      }
    }
  }
  handleNavReparent();
  window.addEventListener('resize', handleNavReparent);

  // ============ SMOOTH ANCHOR SCROLLING (via Lenis) ============
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const t = document.querySelector(a.getAttribute('href'));
      if (t) {
        e.preventDefault();
        if (lenis) lenis.scrollTo(t, { offset: -80, duration: 1.4 });
        else window.scrollTo({ top: t.offsetTop - 80, behavior: 'smooth' });
      }
    });
  });

  // ============ WORK SCROLL DRAG ============
  const ws = document.getElementById('workScroll');
  if (ws) {
    let down = false, sx, sl;
    ws.addEventListener('mousedown', e => { down = true; sx = e.pageX - ws.offsetLeft; sl = ws.scrollLeft; });
    ws.addEventListener('mouseleave', () => down = false);
    ws.addEventListener('mouseup', () => down = false);
    ws.addEventListener('mousemove', e => { if (!down) return; e.preventDefault(); ws.scrollLeft = sl - (e.pageX - ws.offsetLeft - sx) * 1.5; });

    // Arrow navigation — smooth tracked scrolling
    const SCROLL_AMT = 440;
    let scrollTarget = 0;
    let scrollTween = null;
    const prevBtn = document.getElementById('workPrev');
    const nextBtn = document.getElementById('workNext');

    function smoothScroll(dir) {
      if (scrollTween) scrollTween.kill();
      scrollTarget = Math.max(0, Math.min(ws.scrollWidth - ws.clientWidth, ws.scrollLeft + dir * SCROLL_AMT));
      scrollTween = gsap.to(ws, { scrollLeft: scrollTarget, duration: 1, ease: 'power3.out', onComplete: () => scrollTween = null });
    }

    if (prevBtn) prevBtn.addEventListener('click', () => smoothScroll(-1));
    if (nextBtn) nextBtn.addEventListener('click', () => smoothScroll(1));
  }

  // ============ CONTACT FORM ============
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const btn = form.querySelector('.btn-w');
      const orig = btn.innerHTML;
      btn.innerHTML = '✓ Sent'; btn.style.background = '#00c853'; btn.style.pointerEvents = 'none';
      setTimeout(() => { btn.innerHTML = orig; btn.style.background = ''; btn.style.pointerEvents = ''; form.reset(); }, 2500);
    });
  }

  // ============ DOT GRID (Google Stitch style) ============
  const canvas = document.getElementById('aurora');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let W, H, mouseX = -9999, mouseY = -9999;
    const GAP = 32;             // spacing between dots
    const DOT_R = 1.2;          // base dot radius
    const GLOW_R = 180;         // mouse influence radius
    const BASE_ALPHA = 0.1;     // dim idle dots

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });
    window.addEventListener('mouseleave', () => { mouseX = -9999; mouseY = -9999; });

    function drawGrid() {
      ctx.clearRect(0, 0, W, H);

      const cols = Math.ceil(W / GAP) + 1;
      const rows = Math.ceil(H / GAP) + 1;
      const offsetX = (W % GAP) / 2;
      const offsetY = (H % GAP) / 2;
      const isLight = document.documentElement.classList.contains('light-mode');

      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          const x = offsetX + col * GAP;
          const y = offsetY + row * GAP;

          let currentMouseX = mouseX;
          let currentMouseY = mouseY;
          let dist;
          
          if (W <= 768) {
             // On mobile, create a horizontal scanning wave based on scroll position!
             const scrollMax = Math.max(1, document.body.scrollHeight - window.innerHeight);
             const scrollP = window.scrollY / scrollMax;
             // Glow follows the scroll position from top to bottom of screen
             currentMouseY = scrollP * H;
             // Distance is only based on Y to make a full-width horizontal wave
             dist = Math.abs(y - currentMouseY);
          } else {
             const dx = x - currentMouseX;
             const dy = y - currentMouseY;
             dist = Math.sqrt(dx * dx + dy * dy);
          }

          let alpha = BASE_ALPHA;
          let radius = DOT_R;
          
          let r = isLight ? 0 : 255;
          let g = isLight ? 0 : 255;
          let b = isLight ? 0 : 255;

          if (dist < GLOW_R) {
            const t = 1 - dist / GLOW_R;
            const ease = t * t * (3 - 2 * t); // smoothstep
            alpha = BASE_ALPHA + ease * (isLight ? 0.3 : 0.7);
            radius = DOT_R + ease * 1.2;
            
            if (isLight) {
              // Transition to blue in light mode
              r = Math.round(0 + ease * 0);
              g = Math.round(0 + ease * 85);
              b = Math.round(0 + ease * 255);
            } else {
              // Transition from white to blue in dark mode
              r = Math.round(255 - ease * 255);
              g = Math.round(255 - ease * 170);
              b = 255;
            }
          }

          ctx.beginPath();
          ctx.arc(x, y, radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(${r},${g},${b},${alpha})`;
          ctx.fill();
        }
      }
    }

    function animate() {
      drawGrid();
      requestAnimationFrame(animate);
    }
    animate();
  }

  // ============ ORB PARALLAX ============
  document.querySelectorAll('.orb').forEach(orb => {
    const speed = parseFloat(orb.dataset.speed) || 0.3;
    gsap.to(orb, {
      y: () => -window.innerHeight * speed,
      ease: 'none',
      scrollTrigger: {
        trigger: document.body,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1.5,
      }
    });
  });

  // ============ HERO GLOW PULSE ============
  const heroGlow = document.querySelector('.hero-glow');
  if (heroGlow) {
    gsap.to(heroGlow, {
      scale: 1.15, opacity: 0.6, duration: 4, ease: 'sine.inOut', yoyo: true, repeat: -1,
    });
    gsap.to(heroGlow, {
      opacity: 0,
      scrollTrigger: { trigger: '.hero', start: 'bottom 80%', end: 'bottom 20%', scrub: 1 }
    });
  }

  // ============ NAVBAR MORPHING ============
  const nav = document.querySelector('.nav');
  if (nav) {
    ScrollTrigger.create({
      start: 'top -100',
      end: 99999,
      toggleClass: {className: 'scrolled', targets: '.nav'}
    });
  }

  // ============ MAGNETIC BUTTONS ============
  document.querySelectorAll('[data-magnetic]').forEach(btn => {
    const xTo = gsap.quickTo(btn, "x", {duration: 0.4, ease: "power3"});
    const yTo = gsap.quickTo(btn, "y", {duration: 0.4, ease: "power3"});

    btn.addEventListener("mousemove", (e) => {
      const rect = btn.getBoundingClientRect();
      const hX = e.clientX - (rect.left + rect.width / 2);
      const hY = e.clientY - (rect.top + rect.height / 2);
      xTo(hX * 0.3);
      yTo(hY * 0.3);
    });

    btn.addEventListener("mouseleave", () => {
      xTo(0);
      yTo(0);
    });
  });

  // ============ TOUR GUIDE ============
  const guide = document.querySelector('.tour-guide');
  const guideLine = document.querySelector('.tour-line-fill');
  const guideDot = document.querySelector('.tour-dot');
  const guideLabels = document.querySelectorAll('.tour-marker');

  if (guide && guideLine && guideDot) {
    ScrollTrigger.create({
      trigger: document.body,
      start: 'top top',
      end: 'bottom bottom',
      onUpdate: self => {
        const pct = self.progress * 100;
        guideLine.style.height = pct + '%';
        guideDot.style.top = pct + '%';
      }
    });

    const sections = ['#hero', '#services', '#about', '#work', '#process', '#testimonials', '#faq', '#contact'];

    guideLabels.forEach((marker, i) => {
      const section = document.querySelector(sections[i]);
      if (section) {
        ScrollTrigger.create({
          trigger: section,
          start: 'top center',
          end: 'bottom center',
          onEnter: () => setActiveMarker(i),
          onEnterBack: () => setActiveMarker(i),
        });
      }
    });

    function setActiveMarker(idx) {
      guideLabels.forEach((m, i) => m.classList.toggle('active', i === idx));
    }

    gsap.from(guide, {
      opacity: 0, duration: 1, delay: 1.5,
      scrollTrigger: { trigger: '.hero', start: 'bottom 90%', toggleActions: 'play none none reverse' }
    });
  }

  // ============ MODALS (Privacy Policy + Terms of Service) ============
  function openModal(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    el.addEventListener('click', function onOverlayClick(e) {
      if (e.target === el) closeModal(id);
    }, { once: false });
  }
  function closeModal(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  const openPrivacy = document.getElementById('openPrivacy');
  const openTerms  = document.getElementById('openTerms');
  const closePrivacy = document.getElementById('closePrivacy');
  const closeTerms   = document.getElementById('closeTerms');

  if (openPrivacy) openPrivacy.addEventListener('click', e => { e.preventDefault(); openModal('privacyModal'); });
  if (openTerms)   openTerms.addEventListener('click',   e => { e.preventDefault(); openModal('termsModal');  });
  if (closePrivacy) closePrivacy.addEventListener('click', () => closeModal('privacyModal'));
  if (closeTerms)   closeTerms.addEventListener('click',   () => closeModal('termsModal'));

  // Cookie privacy link also opens privacy modal
  const cookiePrivacyLink = document.getElementById('cookiePrivacyLink');
  if (cookiePrivacyLink) cookiePrivacyLink.addEventListener('click', e => { e.preventDefault(); openModal('privacyModal'); });

  // Escape key closes any open modal
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeModal('privacyModal');
      closeModal('termsModal');
    }
  });

  // ============ COOKIE CONSENT ============
  const cookieBanner  = document.getElementById('cookieBanner');
  const cookieAccept  = document.getElementById('cookieAccept');
  const cookieDecline = document.getElementById('cookieDecline');

  function hideCookieBanner() {
    if (!cookieBanner) return;
    cookieBanner.classList.remove('is-visible');
  }
  function showCookieBanner() {
    if (!cookieBanner) return;
    setTimeout(() => cookieBanner.classList.add('is-visible'), 1200);
  }

  if (cookieBanner) {
    const consent = localStorage.getItem('sk_cookie_consent');
    if (!consent) {
      showCookieBanner();
    }
    if (cookieAccept) {
      cookieAccept.addEventListener('click', () => {
        localStorage.setItem('sk_cookie_consent', 'accepted');
        hideCookieBanner();
      });
    }
    if (cookieDecline) {
      cookieDecline.addEventListener('click', () => {
        localStorage.setItem('sk_cookie_consent', 'declined');
        hideCookieBanner();
      });
    }
  }

});

