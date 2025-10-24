document.addEventListener('DOMContentLoaded', () => {
  // Contador de caracteres y auto-resize
  const txt = document.getElementById('message');
  const count = document.getElementById('count');
  const update = () => {
    count.textContent = String(txt.value.length);
    txt.style.height = 'auto';
    txt.style.height = Math.min(txt.scrollHeight, 400) + 'px';
  };
  txt?.addEventListener('input', update); update();

  // Validación simple en cliente
  const form = document.getElementById('contactForm');
  form?.addEventListener('submit', (e) => {
    const required = ['name','email','subject','message'];
    const invalid = required.some(id => !(document.getElementById(id)?.value || '').trim());
    if (invalid) {
      e.preventDefault();
      alert('Completa todos los campos por favor.');
    }
  });
});