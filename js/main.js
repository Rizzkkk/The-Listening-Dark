/* ===================================================================
   THE LISTENING DARK — shared behaviour
   Progressive enhancement: the site is fully readable without JS.
   All motion respects prefers-reduced-motion.
   Calm build: no grain canvas, no custom cursor, no magnetic buttons.
   =================================================================== */
(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var supportsInert = 'inert' in HTMLElement.prototype;

  /* ---- Nav: scrolled state ---- */
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () {
      if (window.scrollY > 40) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Mobile menu (focus-contained: page behind goes inert) ---- */
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.querySelector('.menu');
  if (toggle && menu) {
    var lastFocus = null;
    var inertTargets = [
      document.getElementById('main'),
      document.querySelector('.brand'),
      document.querySelector('.nav-links')
    ].filter(Boolean);

    var setInert = function (on) {
      if (!supportsInert) return;
      inertTargets.forEach(function (el) {
        if (on) el.setAttribute('inert', '');
        else el.removeAttribute('inert');
      });
    };

    var openMenu = function () {
      lastFocus = document.activeElement;
      document.body.classList.add('menu-open');
      menu.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
      menu.removeAttribute('aria-hidden');
      setInert(true);
      var first = menu.querySelector('a, button');
      if (first) first.focus();
    };
    var closeMenu = function () {
      document.body.classList.remove('menu-open');
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      menu.setAttribute('aria-hidden', 'true');
      setInert(false);
      if (lastFocus) lastFocus.focus();
    };
    toggle.addEventListener('click', function () {
      if (menu.classList.contains('open')) closeMenu(); else openMenu();
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !menu.classList.contains('open')) return;
      closeMenu();
    });
    /* belt-and-braces focus cycle for browsers without inert */
    if (!supportsInert) {
      document.addEventListener('keydown', function (e) {
        if (e.key !== 'Tab' || !menu.classList.contains('open')) return;
        var items = menu.querySelectorAll('a, button');
        if (!items.length) return;
        var list = Array.prototype.slice.call(items);
        list.push(toggle);
        var idx = list.indexOf(document.activeElement);
        var next = e.shiftKey ? idx - 1 : idx + 1;
        if (idx === -1 || next >= list.length || next < 0) {
          e.preventDefault();
          list[e.shiftKey ? list.length - 1 : 0].focus();
        }
      });
    }
    /* recover gracefully if the viewport crosses the desktop breakpoint */
    window.matchMedia('(min-width: 900px)').addEventListener
      ? window.matchMedia('(min-width: 900px)').addEventListener('change', function (mq) {
          if (mq.matches && menu.classList.contains('open')) closeMenu();
        })
      : null;
  }

  /* ---- Hero title: split into letters (one-time entrance) ---- */
  var title = document.querySelector('[data-split]');
  if (title) {
    var txt = title.textContent;
    title.textContent = '';
    var frag = document.createDocumentFragment();
    for (var i = 0; i < txt.length; i++) {
      var c = txt[i];
      if (c === ' ') { frag.appendChild(document.createTextNode(' ')); continue; }
      var s = document.createElement('span');
      s.className = 'ch';
      s.textContent = c;
      if (!reduce) {
        s.style.opacity = '0';
        s.style.transform = 'translateY(0.4em)';
        s.style.transition = 'opacity .8s var(--ease), transform .8s var(--ease)';
        s.style.transitionDelay = (0.25 + i * 0.045) + 's';
      }
      frag.appendChild(s);
    }
    title.appendChild(frag);
    if (!reduce) {
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          var chs = title.querySelectorAll('.ch');
          for (var j = 0; j < chs.length; j++) { chs[j].style.opacity = '1'; chs[j].style.transform = 'none'; }
        });
      });
    }
  }

  /* ---- Sequential reveal on load (hero elements) ---- */
  var seq = document.querySelectorAll('[data-reveal]');
  seq.forEach(function (el, i) {
    if (reduce) return;
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity .9s var(--ease), transform .9s var(--ease)';
    el.style.transitionDelay = (0.15 + i * 0.12) + 's';
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { el.style.opacity = '1'; el.style.transform = 'none'; });
    });
  });

  /* ---- Scroll reveals ---- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.16, rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal, .stagger').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal, .stagger').forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- Cover 3D tilt (desktop hover only, the one kept flourish) ---- */
  var cover = document.getElementById('cover');
  if (cover && fine && !reduce) {
    var stage = cover.parentElement;
    stage.addEventListener('mousemove', function (e) {
      var r = stage.getBoundingClientRect();
      var px = (e.clientX - r.left) / r.width - 0.5;
      var py = (e.clientY - r.top) / r.height - 0.5;
      cover.style.transform = 'rotateY(' + (px * 12) + 'deg) rotateX(' + (-py * 12) + 'deg) translateZ(16px)';
    });
    stage.addEventListener('mouseleave', function () { cover.style.transform = ''; });
  }

  /* ---- Accordions (FAQ / interview) — rapid-click safe ---- */
  document.querySelectorAll('.accordion').forEach(function (acc) {
    acc.querySelectorAll('.acc-item').forEach(function (item) {
      var trigger = item.querySelector('.acc-trigger');
      var panel = item.querySelector('.acc-panel');
      if (!trigger || !panel) return;
      trigger.setAttribute('aria-expanded', 'false');
      trigger.addEventListener('click', function () {
        var isOpen = item.classList.contains('open');
        /* clear any pending transition handler before switching direction */
        if (panel._done) {
          panel.removeEventListener('transitionend', panel._done);
          panel._done = null;
        }
        if (isOpen) {
          panel.style.height = panel.scrollHeight + 'px';
          requestAnimationFrame(function () { panel.style.height = '0px'; });
          item.classList.remove('open');
          trigger.setAttribute('aria-expanded', 'false');
        } else {
          item.classList.add('open');
          trigger.setAttribute('aria-expanded', 'true');
          panel.style.height = panel.scrollHeight + 'px';
          panel._done = function (e) {
            if (e.propertyName !== 'height') return;
            if (item.classList.contains('open')) panel.style.height = 'auto';
            panel.removeEventListener('transitionend', panel._done);
            panel._done = null;
          };
          panel.addEventListener('transitionend', panel._done);
        }
      });
    });
  });

  /* ---- Excerpt gate (reveal the fade-locked passage) ---- */
  document.querySelectorAll('[data-unlock]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      var sel = btn.getAttribute('data-unlock');
      var gate = document.querySelector(sel);
      if (gate) {
        e.preventDefault();
        gate.classList.remove('locked');
        var extra = btn.closest('.gate-cta');
        if (extra) {
          var wrapEl = btn.parentNode;
          if (wrapEl && wrapEl !== extra) wrapEl.style.display = 'none';
          else btn.style.display = 'none';
        }
      }
    });
  });

  /* ---- Email delivery: FormSubmit AJAX → author.kpcap@gmail.com ----
     Free, no account needed. NOTE: the very first submission triggers a
     one-time activation email to that inbox — click "Activate" once and
     every submission after that is delivered normally. */
  var ENDPOINT = 'https://formsubmit.co/ajax/author.kpcap@gmail.com';
  var OWNER = 'author.kpcap@gmail.com';
  var emailRe = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  function deliver(payload, btn, msg, okText) {
    var prev = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    return fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error('bad status');
      return r.json();
    }).then(function () {
      if (msg) { msg.classList.remove('error'); msg.textContent = okText; }
      return true;
    }).catch(function () {
      if (msg) {
        msg.classList.add('error');
        msg.textContent = 'Couldn’t reach the list — please email ' + OWNER + ' and we’ll add you by hand.';
      }
      return false;
    }).finally(function () {
      if (btn) { btn.disabled = false; btn.textContent = prev; }
    });
  }

  document.querySelectorAll('form[data-waitlist]').forEach(function (form) {
    var msg = form.parentNode.querySelector('.form-msg') || form.querySelector('.form-msg');
    var input = form.querySelector('input[type="email"]');
    var btn = form.querySelector('button[type="submit"]');
    var hp = form.querySelector('.hp input');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (hp && hp.value) return; /* honeypot tripped */
      var v = (input.value || '').trim();
      if (!emailRe.test(v)) {
        if (msg) { msg.classList.add('error'); msg.textContent = 'That email doesn’t look right — try again.'; }
        input.focus();
        return;
      }
      deliver({
        _subject: 'Waitlist signup — The Listening Dark',
        _template: 'table',
        _captcha: 'false',
        email: v,
        page: location.pathname.split('/').pop() || 'index.html'
      }, btn, msg, 'You’re on the list. The dark is listening.').then(function (ok) {
        if (ok) form.reset();
      });
    });
  });

  var contact = document.querySelector('form[data-contact]');
  if (contact) {
    var cmsg = contact.querySelector('.form-msg');
    var cbtn = contact.querySelector('button[type="submit"]');
    contact.addEventListener('submit', function (e) {
      e.preventDefault();
      var hp = contact.querySelector('.hp input');
      if (hp && hp.value) return;
      var email = contact.querySelector('#c-email');
      var v = email ? (email.value || '').trim() : '';
      if (!emailRe.test(v)) {
        if (cmsg) { cmsg.classList.add('error'); cmsg.textContent = 'Please enter a valid email so we can reply.'; }
        if (email) email.focus();
        return;
      }
      var val = function (id) { var el = contact.querySelector(id); return el ? el.value.trim() : ''; };
      deliver({
        _subject: 'Contact — The Listening Dark: ' + (val('#c-subject') || 'no subject'),
        _template: 'table',
        _captcha: 'false',
        _replyto: v,
        name: val('#c-name'),
        email: v,
        subject: val('#c-subject'),
        message: val('#c-message')
      }, cbtn, cmsg, 'Message sent. We’ll be in touch.').then(function (ok) {
        if (ok) contact.reset();
      });
    });
  }

  /* ---- Footer year ---- */
  var yr = document.querySelector('[data-year]');
  if (yr) yr.textContent = new Date().getFullYear();
})();
