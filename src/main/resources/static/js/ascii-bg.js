/**
 * Ambient ASCII Art Background Engine
 * Hybrid Bunpro x Neon Database aesthetic
 * Renders a low-CPU, high-contrast, subtle architectural/neural ASCII grid canvas
 */
(function () {
  'use strict';

  function initAsciiBackground() {
    var canvas = document.getElementById('ascii-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'ascii-canvas';
      document.body.prepend(canvas);
    }

    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var chars = ['·', ':', '+', '*', '#', '/', '\\', '|', '-', '=', '%'];
    var fontSize = 14;
    var charWidth = 8.4;
    var charHeight = 16;
    var cols = 0;
    var rows = 0;
    var mouseX = -9999;
    var mouseY = -9999;
    var targetMouseX = -9999;
    var targetMouseY = -9999;
    var time = 0;
    var lastFrameTime = 0;
    var targetFps = 24;
    var frameInterval = 1000 / targetFps;
    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function resize() {
      var dpr = window.devicePixelRatio || 1;
      var w = window.innerWidth;
      var h = window.innerHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      cols = Math.ceil(w / charWidth) + 1;
      rows = Math.ceil(h / charHeight) + 1;
      ctx.font = fontSize + "px 'JetBrains Mono', monospace";
      ctx.textBaseline = 'top';
    }

    window.addEventListener('resize', function () {
      resize();
    });

    window.addEventListener('mousemove', function (e) {
      targetMouseX = e.clientX;
      targetMouseY = e.clientY;
    }, { passive: true });

    document.addEventListener('mouseleave', function () {
      targetMouseX = -9999;
      targetMouseY = -9999;
    });

    resize();

    function render(timestamp) {
      requestAnimationFrame(render);

      if (prefersReducedMotion && lastFrameTime > 0) return;

      var elapsed = timestamp - lastFrameTime;
      if (elapsed < frameInterval) return;
      lastFrameTime = timestamp - (elapsed % frameInterval);

      // Smooth mouse interpolation
      mouseX += (targetMouseX - mouseX) * 0.15;
      mouseY += (targetMouseY - mouseY) * 0.15;

      time += 0.015;

      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

      for (var r = 0; r < rows; r++) {
        var y = r * charHeight;
        for (var c = 0; c < cols; c++) {
          var x = c * charWidth;

          // Wave equation for architectural/topographic shimmer
          var wave1 = Math.sin(c * 0.08 + time * 0.8 + r * 0.04);
          var wave2 = Math.cos(r * 0.1 - time * 0.5 + c * 0.03);
          var combined = (wave1 + wave2) * 0.5;

          // Proximity to cursor
          var dx = x - mouseX;
          var dy = y - mouseY;
          var dist = Math.sqrt(dx * dx + dy * dy);
          var proximity = Math.max(0, 1 - dist / 180);

          var value = (combined + 1) * 0.5 + proximity * 0.6;
          value = Math.max(0, Math.min(1, value));

          var charIndex = Math.floor(value * (chars.length - 1));
          var char = chars[charIndex];

          // Color calculation: very subtle neutral gray by default, emerald phosphor highlight near cursor or peaks
          var baseAlpha = 0.035 + (value * 0.03);

          if (proximity > 0.05 || (value > 0.88 && (c + r) % 5 === 0)) {
            // Neon Phosphor highlight (#00E599)
            var emeraldAlpha = Math.min(0.28, baseAlpha + proximity * 0.35);
            ctx.fillStyle = 'rgba(0, 229, 153, ' + emeraldAlpha.toFixed(3) + ')';
          } else {
            // High-contrast subtle white/slate telemetry
            ctx.fillStyle = 'rgba(148, 163, 184, ' + baseAlpha.toFixed(3) + ')';
          }

          ctx.fillText(char, x, y);
        }
      }
    }

    requestAnimationFrame(render);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAsciiBackground);
  } else {
    initAsciiBackground();
  }
})();
