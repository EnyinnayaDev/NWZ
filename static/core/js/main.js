/* NWZ Nutrition & Wellness — front-end interactions
   - Mobile nav toggle
   - Scroll-reveal animations
   - Animated stat counters
   - Auto-dismissing flash messages
   - Small UX niceties for the booking form
*/

document.addEventListener('DOMContentLoaded', function () {
  initNavToggle();
  initScrollReveal();
  initStatCounters();
  initFlashMessages();
  initBookingFormUX();
});

function initNavToggle() {
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('primaryNav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', function () {
    var isOpen = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggle.classList.toggle('is-active', isOpen);
  });

  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

function initScrollReveal() {
  var items = document.querySelectorAll('[data-reveal]');
  if (!items.length) return;

  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  items.forEach(function (el) { observer.observe(el); });
}

function initStatCounters() {
  var counters = document.querySelectorAll('[data-count-to]');
  if (!counters.length) return;

  var animated = new WeakSet();

  function animateCounter(el) {
    if (animated.has(el)) return;
    animated.add(el);

    var target = parseFloat(el.getAttribute('data-count-to')) || 0;
    var duration = 1100;
    var start = null;

    function step(timestamp) {
      if (!start) start = timestamp;
      var progress = Math.min((timestamp - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); /* ease-out cubic */
      var current = Math.round(target * eased);
      el.textContent = current;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        el.textContent = target;
      }
    }
    window.requestAnimationFrame(step);
  }

  if (!('IntersectionObserver' in window)) {
    counters.forEach(animateCounter);
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(function (el) { observer.observe(el); });
}

function initFlashMessages() {
  var flashes = document.querySelectorAll('[data-flash]');
  flashes.forEach(function (flash) {
    var closeBtn = flash.querySelector('[data-flash-close]');
    var dismiss = function () {
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-6px)';
      setTimeout(function () { flash.remove(); }, 250);
    };
    if (closeBtn) closeBtn.addEventListener('click', dismiss);
    setTimeout(dismiss, 6000);
  });
}

function initBookingFormUX() {
  var dateInput = document.querySelector('#id_date');
  var timeInput = document.querySelector('#id_time');
  if (!dateInput && !timeInput) return;

  /* Keep the date field from ever going into the past, even if the
     page has been open a while (e.g. left open overnight). */
  if (dateInput) {
    var today = new Date();
    var iso = today.toISOString().split('T')[0];
    if (!dateInput.getAttribute('min') || dateInput.getAttribute('min') < iso) {
      dateInput.setAttribute('min', iso);
    }
  }

  /* Gently nudge users back into NWZ's 9am-5pm working hours. */
  if (timeInput) {
    timeInput.addEventListener('change', function () {
      var value = timeInput.value;
      if (!value) return;
      if (value < '09:00') timeInput.value = '09:00';
      if (value > '17:00') timeInput.value = '17:00';
    });
  }
}
