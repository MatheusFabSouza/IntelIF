document.addEventListener('DOMContentLoaded', () => {
  const visibility = document.getElementById('id_visibilidade');
  const turma = document.getElementById('id_turma');
  if (!visibility || !turma) return;
  const group = turma.closest('.field-group');

  const update = () => {
    const show = visibility.value === 'TURMA';
    if (group) group.classList.toggle('d-none', !show);
    turma.required = show;
    if (!show) turma.value = '';
  };

  visibility.addEventListener('change', update);
  update();
});
