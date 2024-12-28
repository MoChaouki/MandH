from .checkout import Checkout
from cart.cart import Cart


# Create context processor so our cart can work on all pages of the site
def checkout(request):
	# Return the default data from our Cart
	return {'checkout': Checkout(request)}