from product.models import Variants
from product.serializers import VariantsSerializer

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        self.cart = self.session.get(CART_SESSION_ID, {})

    def __iter__(self):
        variant_ids = self.cart.keys()
        variants = Variants.objects.filter(id__in=variant_ids)
        cart = self.cart.copy()
        for variant in variants:
            variant_data = VariantsSerializer(variant).data
            variant_data['image_tag'] = variant.image_tag()  # Include image tag data
            cart[str(variant.id)]['variant'] = variant_data
        for item in cart.values():
            item["title"] = item['variant']["title"]
            item["image"] = item['variant']["image_tag"]
            item["price"] = float(item["price"])
            item['total_price'] = float(item['discount_price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, variant, brand, color, size, material, attribute, quantity=1, discount_price=0):
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'brand': brand, 'color': color, 'size': size, 'material': material,
                                     'attribute': attribute, 'quantity': quantity, 'price': str(variant.price), 'discount_price':discount_price}
        else:
            self.cart[variant_id]["quantity"] += quantity
        self.save()

    def remove(self, variant):
        variant_id = str(variant['id'])
        if variant_id in self.cart:
            del self.cart[variant_id]
        self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()


