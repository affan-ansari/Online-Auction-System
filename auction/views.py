from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .mixins import AuctionOwnerRequiredMixin, BidOwnerRequiredMixin, BuyerRequiredMixin, ProductOwnerRequiredMixin, SellerRequiredMixin
from .models import Product, Auction, Bid, ProductImage
from .forms import BidCreateForm, BidUpdateForm, FileFieldForm, ProductCreateForm, ProductUpdateForm, AuctionCreateForm, AuctionUpdateForm


@login_required
def home(request):
    return render(request, 'auction/home.html')

# PRODUCT VIEWS


class ProductListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'Seller':
            product_list = Product.objects.filter(seller=request.user.seller)
            products_type = 'My'
        elif request.user.user_type == 'Buyer':
            product_list = Product.objects.filter(auction__status='live')
            products_type = 'Live'
        paginator = Paginator(product_list, 10)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        return render(request, 'auction/product_list.html', {
            'products': products,
            'products_type': products_type,
        })


class ProductDetailView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        images = product.productimage_set.all()

        return render(request, 'auction/product_detail.html', {
            'product': product,
            'images': images,
        })

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if request.user == product.seller.user:
            product.delete()
            return redirect('products-list')
        else:
            print("NO PERMISSION")
            return redirect('product-detail', pk=pk)


class ProductCreateView(LoginRequiredMixin, SellerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auction_id = request.GET.get('auction_id')
        initial_data = {}
        if auction_id:
            product = get_object_or_404(Auction, id=auction_id)
            initial_data['auction'] = product
        return render(request, 'auction/product_create.html', {
            'form': ProductCreateForm(initial=initial_data),
        })

    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.seller = request.user.seller
            product = form.save()
            images = [ProductImage(product=product, image=image)
                      for image in form.cleaned_data.get('images', [])]
            ProductImage.objects.bulk_create(images)
            return redirect('product-detail', pk=product.pk)

        return self.get(request)


class ProductUpdateView(LoginRequiredMixin, SellerRequiredMixin, ProductOwnerRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductUpdateForm(instance=product)
        if product.auction and product.auction.status in ['live', 'closed']:
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


class ProductOwnedView(LoginRequiredMixin, BuyerRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        buyer = request.user.buyer
        products = Product.objects.filter(
            bid__buyer=buyer, bid__is_winning_bid=True)

        return render(request, 'auction/product_list.html', {
            'products': products,
            'products_type': 'Owned'
        })


# AUCTION VIEWS


class AuctionListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        auction_groups = [
            qs for qs in [
                Auction.objects.filter(is_approved=True, status='live'),
                Auction.objects.filter(is_approved=True, status='inactive'),
                Auction.objects.filter(is_approved=True, status='closed')
            ] if qs.exists()
        ]
        if request.user.user_type == 'Seller':
            pending_auctions = Auction.objects.filter(
                is_approved=False, status='pending')
            if pending_auctions.exists():
                auction_groups.append(pending_auctions)
        return render(request, 'auction/auction_list.html', {'auction_groups': auction_groups})


class AuctionDetailView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=pk)
        product_list = auction.product_set.all()
        paginator = Paginator(product_list, 2)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        return render(request, 'auction/auction_detail.html', {
            'auction': auction,
            'products': products
        })

    def post(self, request, pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=pk)
        if request.user == auction.seller.user:
            auction.delete()
            return redirect('auctions-list')
        else:
            print("NO PERMISSION")
            return redirect('auction-detail', pk=pk)


class AuctionCreateView(LoginRequiredMixin, SellerRequiredMixin, View):
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


class AuctionUpdateView(LoginRequiredMixin, SellerRequiredMixin, AuctionOwnerRequiredMixin, View):

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


class BidListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'Seller':
            bids = Bid.objects.filter(product__seller__user=request.user)
        elif request.user.user_type == 'Buyer':
            bids = Bid.objects.filter(buyer=request.user.buyer)
        return render(request, 'auction/bid_list.html', {
            'bids': bids,
        })


class BidDetailView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=pk)

        return render(request, 'auction/bid_detail.html', {
            'bid': bid,
        })

    def post(self, request, pk, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=pk)
        if request.user == bid.buyer.user:
            bid.delete()
            return redirect('bids-list')
        else:
            print("NO PERMISSION")
            return redirect('bid-detail', pk=pk)


class BidCreateView(LoginRequiredMixin, BuyerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        initial_data = {}
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            initial_data['product'] = product
        return render(request, 'auction/bid_create.html', {
            'form': BidCreateForm(initial=initial_data),
        })

    def post(self, request, *args, **kwargs):
        form = BidCreateForm(data=request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            buyer = request.user.buyer
            bid_amount = form.cleaned_data['amount']
            existing_bid = Bid.objects.filter(
                buyer=buyer, product=product).first()
            if existing_bid and bid_amount > existing_bid.amount:
                existing_bid.amount = form.cleaned_data['amount']
                existing_bid.save()
                return redirect('bid-detail', pk=existing_bid.pk)
            elif not existing_bid and bid_amount >= product.minimum_bid:
                form.instance.buyer = request.user.buyer
                bid = form.save()
                return redirect('bid-detail', pk=bid.pk)

        return self.get(request)


class BidUpdateView(LoginRequiredMixin, BuyerRequiredMixin, BidOwnerRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=pk)
        form = BidUpdateForm(instance=bid)
        return render(request, 'auction/bid_update.html', {
            'bid': bid,
            'form': form,
        })

    def post(self, request, pk, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=pk)
        form = BidUpdateForm(instance=bid, data=request.POST)
        if form.is_valid():
            if form.cleaned_data['amount'] >= bid.product.minimum_bid:
                form.save()
                return redirect('bid-detail', pk=bid.pk)

        return self.get(request, pk)
