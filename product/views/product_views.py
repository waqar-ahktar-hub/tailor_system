"""Product related views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import View

from product.forms import ProductForm
from product.models import Product, ProductImages


class ProductListView(LoginRequiredMixin, View):
    """List products view."""

    def get(self, request):
        """Render product list template.."""
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return render(request, 'product/list-products.html', context)


product_list_view = ProductListView.as_view()


class ProductDetailView(LoginRequiredMixin, View):
    """Get product view."""

    def get(self, request, id):
        """Render product detail template.."""
        product = get_object_or_404(Product, id=id)
        product_images = ProductImages.objects.filter(product=product).first()
        if product_images:
            product_images_dict = model_to_dict(product_images)
            product_images_dict.pop('id')
            product_images_dict.pop('product')
        else:
            product_images_dict = {}
        context = {
            'product': product,
            'product_images': product_images,
            'product_images_dict': product_images_dict
        }
        return render(request, 'product/product-detail.html', context)


product_detail_view = ProductDetailView.as_view()


class ProductDeleteView(LoginRequiredMixin, View):
    """Delete product view."""

    def post(self, request):
        """Delete product."""
        id = request.POST.get('id')
        get_object_or_404(Product, id=id).delete()
        return redirect('product:products')


product_delete_view = ProductDeleteView.as_view()


class ProductAddView(LoginRequiredMixin, View):
    """Class based view for adding new product."""

    def get(self, request):
        """Return add new product form."""
        form = ProductForm()
        return render(request, 'product/add-product.html',
                      {'form': form, 'func': 'Add'})

    def post(self, request):
        """Save product and redirect to product list."""
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            return redirect('product:product_images_add', product_id=new_product.id)
        else:
            return render(request, 'product/add-product.html', {'form': form, 'func': 'Add'})


product_add_view = ProductAddView.as_view()


class ProductUpdateView(LoginRequiredMixin, View):
    """Class based view for Updating new product."""

    def get(self, request, id):
        """Return Update new product form."""
        product = get_object_or_404(Product, id=id)
        form = ProductForm(instance=product)
        return render(request, 'product/add-product.html',
                      {'form': form, 'func': 'Update', 'product': product})

    def post(self, request, id):
        """Update product and redirect to product list."""
        product = get_object_or_404(Product, id=id)
        form = ProductForm(request.POST, instance=product)
        has_images = ProductImages.objects.filter(product=product).exists()
        if form.is_valid():
            new_product = form.save()
            if has_images:
                return redirect('product:product_images_update', product_id=new_product.id)
            else:
                return redirect('product:product_images_add', product_id=new_product.id)
        else:
            return render(request, 'product/add-product.html', {'form': form, 'func': 'Update', 'product': product})


product_update_view = ProductUpdateView.as_view()
