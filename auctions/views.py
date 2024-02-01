from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Category

class ListingForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Give it a title'
        })
    )
    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Tell more about the product',
            'rows': '3'
        })
    )
    starting_bid = forms.DecimalField(
        label='Starting Bid',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'e.g. 100.00',
            'min': '0.01',
            'max': '999999.99',
            'step': '0.01'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category or write a new one below in 'Other category'",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-group',
        })
    )

    other_category = forms.CharField(
        label='Other Category',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Enter a new category'
        })
    )

    image = forms.URLField(
        label='Image URL',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Image URL (optional)',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        other_category = cleaned_data.get('other_category')

        if not category and not other_category:
            raise forms.ValidationError('Please select a category or enter a new one.')

        if category and other_category:
            raise forms.ValidationError('Please select only one category.')
        
        if other_category:
            cleaned_data['other_category'] = other_category.capitalize()

        return cleaned_data


class BidForm(forms.Form):
    bid_amount = forms.DecimalField(
        label='Bid Amount',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Enter your bid amount',
            'min': '0.01',
            'step': '0.01'
        })
    )

    def clean_bid_amount(self):
        bid_amount = self.cleaned_data['bid_amount']
        max_allowed_value = 999999.99
        if bid_amount <= 0:
            raise forms.ValidationError('Your bid must be greater than zero.')
        elif bid_amount > max_allowed_value:
            raise forms.ValidationError('Your bid must be less than 999999.99.')
        return bid_amount

class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Add a comment...'
        })
    )

def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(status=True).order_by('-date')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            selected_category = form.cleaned_data['category']
            other_category = form.cleaned_data['other_category']

            if not selected_category and other_category:
                new_category, created = Category.objects.get_or_create(name=other_category)
                selected_category = new_category

            listing = Listing(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                starting_bid=form.cleaned_data['starting_bid'],
                price=form.cleaned_data['starting_bid'],
                category=selected_category,
                image=form.cleaned_data['image'],
                author=request.user
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                'form': form
            })
    else:
        return render(request, "auctions/create_listing.html", {
            'form': ListingForm()
        })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid_form = BidForm()
    comment_form = CommentForm()

    if request.method == "POST":
        if request.user.is_authenticated:
            if "bid" in request.POST:
                bid_form = BidForm(request.POST)
                if bid_form.is_valid():
                    bid_amount = bid_form.cleaned_data['bid_amount']
                    if bid_amount > listing.price:
                        bid = Bid(user=request.user, listing=listing, bid=bid_amount)
                        bid.save()
                        listing.price = bid_amount
                        listing.save()
                        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                    else:
                        return render(request, "auctions/listing.html", {
                            'listing': listing,
                            'bid_form': bid_form,
                            'comment_form': comment_form,
                            'error_message': 'Your bid must be greater than the current highest bid.'
                        })
                else:
                    return render(request, "auctions/listing.html", {
                        'listing': listing,
                        'bid_form': bid_form,
                        'comment_form': comment_form,
                        'error_message': 'Invalid bid amount. Please enter a valid amount.'
                    })

            elif "comment" in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment_text = comment_form.cleaned_data['comment']
                    comment = Comment(user=request.user, listing=listing, comment=comment_text)
                    comment.save()
                    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                else:
                    return render(request, "auctions/listing.html", {
                        'listing': listing,
                        'bid_form': bid_form,
                        'comment_form': comment_form,
                        'error_message': 'Invalid comment. Please enter a valid comment.'
                    })

    comments = Comment.objects.filter(listing=listing)

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'bid_form': bid_form,
        'comment_form': comment_form,
        'comments': comments
    })

@login_required(login_url='/login')
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.status = False
        highest_bid = listing.bids.order_by('-bid').first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    

@login_required(login_url='/login')
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        request.user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    
@login_required(login_url='/login')
def remove_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    

@login_required(login_url='/login')
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'listings': request.user.watchlist.all()
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })

def category_listings(request, category_name):
    listings = Listing.objects.filter(category__name=category_name, status=True)
    return render(request, 'auctions/category_listings.html', {
        'listings': listings, 
        'category_name': category_name
    })
