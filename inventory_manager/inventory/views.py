from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Movement
from .forms import ProductForm, MovementForm

# =========================
# CRUD PRODUCTOS
# =========================

# SELECT
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


# CREATE
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})


# UPDATE
def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})


# DELETE
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


# =========================
# CRUD MOVIMIENTOS
# =========================

def movement_list(request):
    movements = Movement.objects.select_related('product').all()
    return render(request, 'inventory/movement_list.html', {'movements': movements})


def movement_create(request):
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movement_list')
    else:
        form = MovementForm()
    return render(request, 'inventory/movement_form.html', {'form': form})


def movement_delete(request, id):
    movement = get_object_or_404(Movement, id=id)
    if request.method == 'POST':
        movement.delete()
        return redirect('movement_list')
    return render(request, 'inventory/movement_confirm_delete.html', {'movement': movement})