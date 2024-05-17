from django.shortcuts import render, get_object_or_404, HttpResponse
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from xhtml2pdf import pisa
from django.utils.translation import gettext as _

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, _("Beer added to cart..."))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, _("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request, _("Your Cart Has Been Updated..."))
        return response

def pdf(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    context = {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
    }
    html_template = 'pdf.html'
    html_content = render(request, html_template, context)
    response = HttpResponse(content_type='application/cart/pdf')
    response['Content-Disposition'] = 'attachment; filename="Factura.pdf"'
    pisa_status = pisa.CreatePDF(html_content.content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating invoice: %s' % pisa_status.err)
    return response
