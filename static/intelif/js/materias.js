document.addEventListener('DOMContentLoaded', () => {
  const search = document.getElementById('subjectSearch');
  const cards = [...document.querySelectorAll('.subject-card')];
  const empty = document.getElementById('searchEmpty');
  const label = document.getElementById('filterLabel');
  let filter = 'all';

  const apply = () => {
    const term = (search?.value || '').trim().toLocaleLowerCase('pt-BR');
    let visible = 0;

    cards.forEach((card) => {
      const matchesText = card.dataset.name.includes(term);
      const matchesFilter = filter === 'all' || (filter === 'next' && card.dataset.next === 'yes') || (filter === 'none' && card.dataset.next === 'no');
      const show = matchesText && matchesFilter;
      card.classList.toggle('d-none', !show);
      if (show) visible += 1;
    });

    if (empty) empty.classList.toggle('d-none', visible !== 0 || cards.length === 0);
  };

  search?.addEventListener('input', apply);
  document.querySelectorAll('.subject-filter-option').forEach((option) => {
    option.addEventListener('click', () => {
      filter = option.dataset.filter;
      if (label) label.textContent = option.textContent.trim();
      apply();
    });
  });
});
