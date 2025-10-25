document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.btn-cart, .add-to-cart');
  if (!buttons.length) return;

  function getCookie(name) {
    const v = document.cookie || '';
    return v.split(';').map(c => c.trim()).find(c => c.startsWith(name + '='))?.split('=').slice(1).join('=') || null;
  }
  const csrftoken = getCookie('csrftoken');

  // Detecta si tu app cuelga de /store/ o de /
  const ADD_URL = window.location.pathname.startsWith('/store/')
    ? '/store/add_to_cart/'
    : '/add_to_cart/';

  buttons.forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();

      const card = button.closest('.card-offer, .product-card');
      if (!card) { alert('No se encontró la tarjeta del producto.'); return; }

      const nameEl  = card.querySelector('.title, .product-title');
      const priceEl = card.querySelector('.new, .sale-price, .price, .final-price');

      const productName  = (nameEl?.textContent || '').trim();
      const rawPrice     = (priceEl?.textContent || '').replace(/[Q$,]/g, '').trim();
      const productPrice = rawPrice || '0';
      const productId    = card.dataset.id || (productName || 'item').replace(/\s+/g,'-').toLowerCase();

      try {
        const res = await fetch(ADD_URL, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrftoken ? { 'X-CSRFToken': csrftoken } : {}),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
          },
          body: new URLSearchParams({ id: productId, name: productName, price: productPrice, qty: '1' })
        });

        if (!res.ok) {
          const txt = await res.text();
          console.error('add_to_cart error:', res.status, txt);
          alert('Error al añadir al carrito (HTTP ' + res.status + ').');
          return;
        }

        const data = await res.json().catch(() => ({}));
        if (data.status === 'ok') {
          if (button.innerText) {
            const old = button.innerText;
            button.innerText = '¡Añadido!';
            button.classList.add('btn-success');
            setTimeout(() => { button.innerText = old; button.classList.remove('btn-success'); }, 1200);
          } else {
            alert('Producto añadido.');
          }
        } else {
          alert('No se pudo añadir al carrito.');
        }
      } catch (err) {
        console.error(err);
        alert('Error de red al añadir al carrito.');
      }
    });
  });
});
