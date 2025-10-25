# store/cart.py
from decimal import Decimal
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, name, price, quantity=1):
        product_id = str(product_id)
        item = self.cart.get(product_id, {
            'name': name,
            'price': str(price),  # string para ser serializable
            'quantity': 0,
        })
        item['name'] = name
        item['price'] = str(price)
        item['quantity'] = int(item.get('quantity', 0)) + int(quantity)
        self.cart[product_id] = item
        self.save()

    def set_quantity(self, product_id, quantity):
        product_id = str(product_id)
        qty = max(0, int(quantity))
        if qty <= 0:
            self.cart.pop(product_id, None)
        else:
            if product_id in self.cart:
                self.cart[product_id]['quantity'] = qty
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product_id, step=1):
        product_id = str(product_id)
        if product_id in self.cart:
            current = int(self.cart[product_id].get('quantity', 1))
            new_q = max(0, current - int(step))
            if new_q == 0:
                del self.cart[product_id]
            else:
                self.cart[product]()
