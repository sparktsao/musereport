(() => {
  const search = document.querySelector('#search');
  const topic = document.querySelector('#topic');
  const language = document.querySelector('#language');
  const cards = [...document.querySelectorAll('.report')];
  const status = document.querySelector('.results');
  const empty = document.querySelector('.empty');
  document.querySelector('.filters').hidden = false;

  function filter() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const lang = card.dataset.language;
      const languageMatch = !language.value || (language.value === 'en' ? /English|EN/.test(lang) : /繁/.test(lang));
      const match = terms.every(term => card.dataset.search.toLocaleLowerCase().includes(term)) &&
        (!topic.value || card.dataset.topic === topic.value) && languageMatch;
      card.hidden = !match;
      if (match) count++;
    }
    status.textContent = count === cards.length ? `Showing all ${count} reports` : `Showing ${count} of ${cards.length} reports`;
    empty.hidden = count !== 0;
  }
  search.addEventListener('input', filter);
  topic.addEventListener('change', filter);
  language.addEventListener('change', filter);
  document.querySelector('#reset').addEventListener('click', () => {
    search.value = topic.value = language.value = '';
    filter();
    search.focus();
  });
  filter();
})();
