from django.shortcuts import get_object_or_404, redirect

from auction.models import Auction, Bid, Product


class SellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type == "Seller":
            return super().dispatch(request, *args, **kwargs)
        return redirect('auctions-list')


class BuyerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type == "Buyer":
            return super().dispatch(request, *args, **kwargs)
        return redirect('auctions-list')


class AuctionOwnerRequiredMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        auction = get_object_or_404(Auction, pk=pk)
        if request.user != auction.seller.user:
            return redirect('auctions-list')
        return super().dispatch(request, pk, *args, **kwargs)


class BidOwnerRequiredMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=pk)
        if request.user != bid.buyer.user:
            return redirect('products-list')
        return super().dispatch(request, pk, *args, **kwargs)


class ProductOwnerRequiredMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if request.user != product.seller.user:
            return redirect('products-list')
        return super().dispatch(request, pk, *args, **kwargs)
