document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const toggle = document.getElementById('sidebarToggle');
  const overlay = document.getElementById('mobileOverlay');

  if (!sidebar || !toggle || !overlay) return;

  const setOpen = (open) => {
    sidebar.classList.toggle('is-open', open);
    overlay.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  };

  toggle.addEventListener('click', () => setOpen(!sidebar.classList.contains('is-open')));
  overlay.addEventListener('click', () => setOpen(false));
  sidebar.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    if (window.innerWidth < 992) setOpen(false);
  }));

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 992) setOpen(false);
  });
});
