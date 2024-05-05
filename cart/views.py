
from django.shortcuts import render, get_object_or_404, HttpResponse
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from xhtml2pdf import pisa

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})




def cart_add(request):
	# Get the cart
	cart = Cart(request) 
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product, quantity=product_qty)

		# Get Cart Quantity
		cart_quantity = cart.__len__()

		# Return resonse
		
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Cerveza añadida al carrito..."))
		return response

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response


def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response
	
def pdf(request):
    # Create a Cart instance
    cart = Cart(request)
    
    # Retrieve cart products, quantities, and totals
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    # Pass the necessary data to the HTML template
    context = {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
    }

    # Render the HTML template with the data
    html_template = 'pdf.html'
    html_content = render(request, html_template, context)

    # Generate PDF
    response = HttpResponse(content_type='application/cart/pdf')
    response['Content-Disposition'] = 'attachment; filename="Factura.pdf"'

    pisa_status = pisa.CreatePDF(html_content.content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar la factura: %s' % pisa_status.err)

    return response