from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Product, Auction, Bid
from .forms import ProductCreateForm, ProductUpdateForm, AuctionCreateForm, AuctionUpdateForm


@login_required
def home(request):
    return render(request, 'auction/home.html')

# PRODUCT VIEWS


class ProductListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'auction/product_list.html', {
            'products': Product.objects.all(),
        })


class ProductDetailView(View):

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)

        return render(request, 'auction/product_detail.html', {
            'product': product,
        })


class ProductCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'auction/product_create.html', {
            'form': ProductCreateForm(),
        })

    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            form.instance.seller = request.user.seller
            product = form.save()
            return redirect('product-detail', pk=product.pk)

        return self.get(request)


class ProductUpdateView(View):

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductUpdateForm(instance=product)
        form.fields['auction'].disabled = True
        return render(request, 'auction/product_update.html', {
            'product': product,
            'form': form,
        })

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductUpdateForm(instance=product, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-detail', pk=product.pk)

        return self.get(request, pk)

# AUCTION VIEWS


class AuctionListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'auction/auction_list.html', {
            'auctions': Auction.objects.all(),
        })


class AuctionDetailView(View):

    def get(self, request, pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=pk)

        return render(request, 'auction/auction_detail.html', {
            'auction': auction,
        })


class AuctionCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'auction/auction_create.html', {
            'form': AuctionCreateForm(),
        })

    def post(self, request, *args, **kwargs):
        form = AuctionCreateForm(data=request.POST)
        if form.is_valid():
            form.instance.seller = request.user.seller
            auction = form.save()
            return redirect('auction-detail', pk=auction.pk)

        return self.get(request)


class AuctionUpdateView(View):

    def get(self, request, pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionUpdateForm(instance=auction, initial={
                                 'start_time': auction.start_time, 'end_time': auction.end_time})
        return render(request, 'auction/auction_update.html', {
            'auction': auction,
            'form': form,
        })

    def post(self, request, pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionUpdateForm(instance=auction, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('auction-detail', pk=auction.pk)

        return self.get(request, pk)

# BID VIEWS