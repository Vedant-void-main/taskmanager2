/* ═══════════════════════════════════════
   TASKMASTER — MAIN JAVASCRIPT
   ═══════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── DARK MODE ──────────────────────────
  const html        = document.documentElement;
  const darkToggle  = document.getElementById('darkToggle');
  const darkIcon    = document.getElementById('darkIcon');

  // Read preference: from server (data attr) or localStorage
  const savedTheme = localStorage.getItem('tm_theme') || 'light';
  applyTheme(savedTheme);

  if (darkToggle) {
    darkToggle.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('tm_theme', next);

      // Persist to server
      const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
      if (csrf) {
        fetch('/users/toggle-dark-mode/', {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf.value, 'Content-Type': 'application/json' },
        });
      }
    });
  }

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    if (darkIcon) {
      darkIcon.className = theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars';
    }
  }

  // ── MOBILE SIDEBAR ──────────────────────
  const sidebarToggle  = document.getElementById('sidebarToggle');
  const sidebar        = document.getElementById('sidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', openSidebar);
  }
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
  }

  function openSidebar() {
    sidebar && sidebar.classList.add('open');
    sidebarOverlay && sidebarOverlay.classList.add('show');
  }
  function closeSidebar() {
    sidebar && sidebar.classList.remove('open');
    sidebarOverlay && sidebarOverlay.classList.remove('show');
  }

  // ── NOTIFICATION PANEL ──────────────────
  const notifBell  = document.getElementById('notifBell');
  const notifPanel = document.getElementById('notifPanel');
  const notifCount = document.getElementById('notifCount');
  const notifList  = document.getElementById('notifList');

  if (notifBell && notifPanel) {
    notifBell.addEventListener('click', (e) => {
      e.stopPropagation();
      notifPanel.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (!notifPanel.contains(e.target) && !notifBell.contains(e.target)) {
        notifPanel.classList.remove('open');
      }
    });
  }

  // ── NOTIFICATION POLLING ────────────────
  // Only poll when user is authenticated (sidebar visible)
  if (document.getElementById('sidebar')) {
    checkNotifications();
    setInterval(checkNotifications, 60000); // every 60s
  }

  let lastAlertSignature = '';

  function checkNotifications() {
    fetch('/tasks/notifications/')
      .then(r => r.json())
      .then(data => {
        const alerts = data.alerts || [];
        const sig = JSON.stringify(alerts);

        // Update notification panel
        if (notifList) {
          if (alerts.length === 0) {
            notifList.innerHTML = '<p class="notif-empty">All caught up! ✓</p>';
          } else {
            notifList.innerHTML = alerts.map(a => `
              <div class="notif-item type-${a.type}">
                <div class="notif-item-icon">${a.icon}</div>
                <div>
                  <div class="notif-item-title">${a.title}</div>
                  <div class="notif-item-msg">${a.message}</div>
                </div>
              </div>
            `).join('');
          }
        }

        // Update badge
        if (notifCount) {
          if (alerts.length > 0) {
            notifCount.textContent = alerts.length;
            notifCount.classList.remove('d-none');
          } else {
            notifCount.classList.add('d-none');
          }
        }

        // Show toast only for NEW notifications
        if (sig !== lastAlertSignature && alerts.length > 0) {
          lastAlertSignature = sig;
          // Only show toast if page is loaded (not first poll after login showing messages)
          if (document.readyState === 'complete') {
            showToastBanner(alerts[0]);
          }

          // Browser Notification API (if permitted)
          if ('Notification' in window && Notification.permission === 'granted') {
            alerts.forEach(a => {
              new Notification(`TaskMaster: ${a.title}`, {
                body: a.message,
                icon: '/static/favicon.ico',
              });
            });
          }
        }
      })
      .catch(() => {}); // Fail silently
  }

  // Request browser notification permission
  if ('Notification' in window && Notification.permission === 'default') {
    setTimeout(() => {
      Notification.requestPermission();
    }, 3000);
  }

  // ── TOAST BANNER ────────────────────────
  function showToastBanner(alert) {
    const container = getOrCreateToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast-msg toast-${alert.type} show`;
    toast.innerHTML = `
      <span>${alert.icon} <strong>${alert.title}:</strong> ${alert.message}</span>
      <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.5s';
      setTimeout(() => toast.remove(), 500);
    }, 6000);
  }

  function getOrCreateToastContainer() {
    let c = document.querySelector('.messages-container');
    if (!c) {
      c = document.createElement('div');
      c.className = 'messages-container';
      const topbar = document.querySelector('.topbar');
      topbar ? topbar.insertAdjacentElement('afterend', c) : document.body.prepend(c);
    }
    return c;
  }

  // ── AUTO-DISMISS MESSAGES ───────────────
  document.querySelectorAll('.toast-msg').forEach(msg => {
    setTimeout(() => {
      msg.style.opacity = '0';
      msg.style.transition = 'opacity 0.5s';
      setTimeout(() => msg.remove(), 500);
    }, 5000);
  });

  // ── TASK TOGGLE AJAX ────────────────────
  document.querySelectorAll('.toggle-form').forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const url  = form.action;
      const csrf = form.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf },
      })
      .then(r => r.json())
      .then(data => {
        const card     = form.closest('.task-card, .dash-task-item');
        const checkbox = form.querySelector('.task-checkbox');

        if (data.status === 'completed') {
          checkbox && checkbox.classList.add('checked');
          checkbox && (checkbox.textContent = '✓');
          card && card.classList.add('task-completed');
          showToastBanner({ type: 'success', icon: '✅', title: 'Done!', message: `"${data.title}" marked complete.` });
        } else {
          checkbox && checkbox.classList.remove('checked');
          checkbox && (checkbox.textContent = '');
          card && card.classList.remove('task-completed');
          showToastBanner({ type: 'info', icon: '🔄', title: 'Reopened', message: `"${data.title}" marked pending.` });
        }
      })
      .catch(() => form.submit()); // Fallback to full page submit
    });
  });

  // ── ANIMATE PROGRESS BAR ────────────────
  const progressFill = document.querySelector('.progress-fill');
  if (progressFill) {
    const target = progressFill.style.width;
    progressFill.style.width = '0%';
    setTimeout(() => { progressFill.style.width = target; }, 200);
  }

  // ── DATE INPUT DEFAULT ───────────────────
  // Pre-fill date inputs with today's date if empty
  document.querySelectorAll('input[type="date"]').forEach(input => {
    if (!input.value && input.name === 'due_date') {
      const today = new Date().toISOString().split('T')[0];
      // Don't force-fill, but set min date
      input.setAttribute('min', today);
    }
  });

});
