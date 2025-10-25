document.addEventListener('DOMContentLoaded', () => {
  // ===== Modo oscuro persistente =====
  const btn  = document.getElementById('themeBtn');
  const icon = document.getElementById('themeIcon');

  const applyIcon = () => {
    const dark = document.body.classList.contains('dark-mode');
    icon?.classList.toggle('fa-moon', !dark);
    icon?.classList.toggle('fa-sun',  dark);
  };

  if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
  }
  applyIcon();

  btn?.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const dark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', dark ? 'enabled' : 'disabled');
    applyIcon();
  });

  // ===== Filtros de categoría =====
  const buttons = document.querySelectorAll('.filter-btn');
  const cards   = document.querySelectorAll('.card-offer');

  const applyFilter = (value) => {
    cards.forEach(card => {
      const ok = (value === 'all') || (card.dataset.category === value);
      card.style.display = ok ? '' : 'none';
    });
  };
  applyFilter('all');

  buttons.forEach(b => {
    b.addEventListener('click', () => {
      buttons.forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      applyFilter(b.dataset.filter || 'all');
    });
  });

  // ===== Countdown 5 días =====
  const dEl = document.getElementById('cd-days'),
        hEl = document.getElementById('cd-hours'),
        mEl = document.getElementById('cd-min'),
        sEl = document.getElementById('cd-sec');

  if (dEl && hEl && mEl && sEl){
    const target = new Date(); target.setDate(target.getDate()+5);
    const tick = () => {
      const diff = target - new Date();
      const z = v => String(Math.max(0,v)).padStart(2,'0');
      if (diff <= 0) { dEl.textContent=hEl.textContent=mEl.textContent=sEl.textContent='00'; return; }
      const d = Math.floor(diff/86400000);
      const h = Math.floor(diff%86400000/3600000);
      const m = Math.floor(diff%3600000/60000);
      const s = Math.floor(diff%60000/1000);
      dEl.textContent=z(d); hEl.textContent=z(h); mEl.textContent=z(m); sEl.textContent=z(s);
    };
    tick(); setInterval(tick, 1000);
  }

  // ===== Newsletter demo =====
  const form = document.querySelector('.newsletter form');
  form?.addEventListener('submit', e=>{
    e.preventDefault();
    const email = form.querySelector('input')?.value || '';
    alert(`¡Gracias por suscribirte con ${email}!`);
    form.reset();
  });

  // ===== Botón "Añadir al carrito" demo =====
  document.querySelectorAll('.btn-cart').forEach(b=>{
    b.addEventListener('click', ()=>{
      b.textContent='¡Añadido!';
      b.style.background='var(--discount)';
      setTimeout(()=>{ b.textContent='Añadir al carrito'; b.style.background='var(--secondary)'; }, 1800);
    });
  });
});
