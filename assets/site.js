(() => {
  const root = document.documentElement;
  const theme = document.querySelector('#theme');
  function setTheme(value) {
    root.dataset.theme = value;
    const label = value === 'dark' ? 'Switch to light theme' : 'Switch to dark theme';
    theme.setAttribute('aria-label', label);
    theme.title = label;
  }
  let stored;
  try { stored = localStorage.getItem('linux-cli-theme'); } catch {}
  setTheme(stored === 'dark' || stored === 'light' ? stored :
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  theme.addEventListener('click', () => {
    setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
    try { localStorage.setItem('linux-cli-theme', root.dataset.theme); } catch {}
  });

  const menu = document.querySelector('#menu');
  const nav = document.querySelector('#nav-links');
  function showMenu(open) {
    nav.classList.toggle('open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menu.addEventListener('click', () => showMenu(!nav.classList.contains('open')));
  nav.addEventListener('click', event => { if (event.target.closest('a')) showMenu(false); });
  function activeSection(id) {
    for (const link of nav.querySelectorAll('a')) {
      if (link.hash === '#' + id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  }
  const navSections = [...document.querySelectorAll('main section[id]')];
  let pending = false;
  const top = document.querySelector('#to-top');
  function updateScroll() {
    top.hidden = scrollY < Math.min(650, innerHeight * .75);
    const current = navSections.filter(section => section.getBoundingClientRect().top <= 160).at(-1);
    const atEnd = scrollY + innerHeight >= document.documentElement.scrollHeight - 2;
    const requested = navSections.find(section => '#' + section.id === location.hash);
    const requestedTop = requested?.getBoundingClientRect().top;
    let selected = current || navSections[0];
    if (atEnd) {
      selected = requestedTop >= 0 && requestedTop < innerHeight ? requested : navSections.at(-1);
    }
    activeSection(selected.id);
    pending = false;
  }
  addEventListener('scroll', () => {
    if (!pending) { pending = true; requestAnimationFrame(updateScroll); }
  }, {passive: true});
  addEventListener('resize', updateScroll);
  addEventListener('hashchange', updateScroll);
  addEventListener('pageshow', updateScroll);
  updateScroll();
  top.addEventListener('click', () => scrollTo({top: 0}));

  const figures = [...document.querySelectorAll('.gallery figure')];
  const search = document.querySelector('#gallery-search');
  const category = document.querySelector('#category');
  const count = document.querySelector('#gallery-count');
  const viewer = document.querySelector('#viewer');
  const image = document.querySelector('#viewer-image');
  const caption = document.querySelector('#viewer-caption');
  const position = document.querySelector('#viewer-position');
  const zoom = document.querySelector('#zoom');
  const box = image.parentElement;
  let visible = [];
  let selected = 0;
  let opener;
  let touch;
  function filter() {
    const term = search.value.trim().toLowerCase();
    visible = figures.filter(figure => {
      const match = (!category.value || figure.dataset.category === category.value) &&
        figure.textContent.toLowerCase().includes(term);
      figure.hidden = !match;
      return match;
    });
    count.textContent = visible.length + ' of ' + figures.length + ' figures';
  }
  function setZoom(enabled) {
    box.classList.toggle('zoomed', enabled);
    box.scrollTo(0, 0);
    zoom.setAttribute('aria-pressed', String(enabled));
    zoom.textContent = enabled ? 'Reset zoom' : 'Zoom';
  }
  function select(index) {
    selected = (index + visible.length) % visible.length;
    const figure = visible[selected];
    image.src = figure.querySelector('a').href;
    image.alt = figure.querySelector('img').alt;
    caption.textContent = figure.querySelector('figcaption span').textContent;
    position.textContent = image.alt + ' (' + (selected + 1) + '/' + visible.length + ')';
    document.querySelector('#previous').disabled = visible.length < 2;
    document.querySelector('#next').disabled = visible.length < 2;
    setZoom(false);
  }
  search.addEventListener('input', filter);
  category.addEventListener('change', filter);
  filter();
  figures.forEach(figure => figure.querySelector('a').addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = event.currentTarget;
    select(visible.indexOf(figure));
    viewer.showModal();
    document.querySelector('#close-viewer').focus();
  }));
  document.querySelector('#previous').addEventListener('click', () => select(selected - 1));
  document.querySelector('#next').addEventListener('click', () => select(selected + 1));
  document.querySelector('#close-viewer').addEventListener('click', () => viewer.close());
  zoom.addEventListener('click', () => setZoom(zoom.getAttribute('aria-pressed') !== 'true'));
  viewer.addEventListener('close', () => opener?.focus());
  document.addEventListener('keydown', event => {
    if (viewer.open && ['ArrowLeft', 'ArrowRight'].includes(event.key)) {
      event.preventDefault();
      select(selected + (event.key === 'ArrowLeft' ? -1 : 1));
    } else if (event.key === 'Escape' && nav.classList.contains('open')) {
      showMenu(false);
      menu.focus();
    }
  });
  box.addEventListener('touchstart', event => {
    touch = [event.changedTouches[0].clientX, event.changedTouches[0].clientY];
  }, {passive: true});
  box.addEventListener('touchend', event => {
    if (!touch || box.classList.contains('zoomed')) return;
    const x = event.changedTouches[0].clientX - touch[0];
    const y = event.changedTouches[0].clientY - touch[1];
    if (Math.abs(x) > 50 && Math.abs(x) > Math.abs(y)) select(selected + (x < 0 ? 1 : -1));
  }, {passive: true});

  const students = JSON.parse(document.querySelector('#student-data').textContent);
  const minimum = document.querySelector('#minimum');
  const average = document.querySelector('#student-summary');
  const rows = document.querySelector('#student-rows');
  function showStudents() {
    const threshold = minimum.value === '' ? 0 : Number(minimum.value);
    const selectedStudents = students.filter(student => student.score >= threshold);
    rows.replaceChildren();
    for (const student of selectedStudents) {
      const row = document.createElement('tr');
      for (const key of ['name', 'program', 'city', 'score']) {
        const cell = document.createElement('td');
        cell.textContent = student[key];
        row.append(cell);
      }
      rows.append(row);
    }
    const mean = selectedStudents.length ?
      (selectedStudents.reduce((sum, student) => sum + student.score, 0) / selectedStudents.length).toFixed(3) : '—';
    average.textContent = selectedStudents.length + ' records · average score ' + mean;
  }
  minimum.addEventListener('input', showStudents);
  showStudents();
})();
