// store/static/store/js/cart_page.js
document.addEventListener('DOMContentLoaded', () => {
  const csrfInput = document.querySelector('input[name=csrfmiddlewaretoken]');
  const csrf = csrfInput ? csrfInput.value : null;

  document.querySelectorAll('form.frm-remove').forEach(frm => {
    frm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const pid = frm.dataset.id;
      const res = await fetch('/store/cart/remove/', {
        method: 'POST',
        headers: csrf ? {'X-CSRFToken': csrf} : {},
        body: new URLSearchParams({id: pid})
      });
      const data = await res.json();
      if (data.ok) {
        // Quita la fila visualmente
        const row = frm.closest('tr');
        if (row) row.remove();
        // Si ya no hay filas, recarga para mostrar "carrito vacío"
        if (!document.querySelector('tbody tr')) location.reload();
      }
    });
  });
});
