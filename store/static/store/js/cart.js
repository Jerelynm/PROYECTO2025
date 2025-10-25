// static/store/js/cart.js
document.addEventListener('DOMContentLoaded', function () {
  // Soporta .btn-cart (tu HTML actual) y .add-to-cart (por si hay otros)
  const buttons = document.querySelectorAll('.btn-cart, .add-to-cart');
  if (!buttons.length) return; // no hay botones en esta página

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // Soporta dos estructuras de tarjeta: .card-offer y .product-card
      const card = button.closest('.card-offer, .product-card');
      if (!card) return;

      // Nombre: .title (nuestro HTML) o .product-title (el viejo)
      const nameEl = card.querySelector('.title, .product-title');
      // Precio: .new (nuestro HTML) o .sale-price (el viejo)
      const priceEl = card.querySelector('.new, .sale-price');

      const productName = (nameEl?.textContent || '').trim();
      const rawPrice = (priceEl?.textContent || '').replace(/[Q,\s]/g, '');
      const productPrice = rawPrice || '0';

      // ID temporal (si luego tienes IDs reales, úsalo desde data-* o backend)
      const productId = card.dataset.id || Math.random().toString(36).slice(2, 8);

      fetch('/store/add_to_cart/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ id: productId, name: productName, price: productPrice })
      })
      .then(r => r.json())
      .then(data => {
        if (data.status === 'ok') {
          // feedback visual
          const original = button.textContent;
          button.textContent = '¡Añadido!';
          button.style.backgroundColor = 'var(--discount)';
          setTimeout(() => {
            button.textContent = original;
            button.style.backgroundColor = 'var(--secondary)';
          }, 1200);
        } else {
          alert('No pudimos añadir al carrito.');
        }
      })
      .catch(() => alert('Error de red al añadir al carrito.'));
    });
  });

  // --- CSRF helper (Django) ---
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
      document.cookie.split(';').forEach(c => {
        const cookie = c.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        }
      });
    }
    return cookieValue;
  }
});
