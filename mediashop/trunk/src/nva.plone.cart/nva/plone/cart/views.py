from five import grok
from nva.cart import ICartAddable, ICartRetriever, ICartHandler


class AddToCart(grok.View):
    """Add an item to the cart
    """
    grok.name('cart.add')
    grok.context(ICartAddable)

    def update(self):
        self.cart = ICartRetriever(self.request.SESSION)

    def render(self):
        handler = ICartHandler(self.cart)
        handler.addItem(self.context)

        self.redirect(self.url(self.context))
