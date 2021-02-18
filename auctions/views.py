from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListingForm, BiddingForm, CommentForm

from .models import *


def index(request): 

    return render(request, 'auctions/index.html', {
        'headline': 'Active Listings',
        'listings': Listing.objects.filter(closed=False)[::-1],
        'count': request.session.get('count', None),
    })


def categories(request):

    return render(request, 'auctions/categories.html', {
        'categories': Category.objects.all(),
        'count': request.session.get('count', None),
    })


def category(request, name):

    category = Category.objects.get(name=name)

    return render(request, 'auctions/index.html', {
        'headline': category,
        'listings': category.listings.filter(closed=False),
        'count': request.session.get('count', None),
    })


@login_required
def create_listing(request):
    if request.method == 'POST':

        form = CreateListingForm(request.POST)

        if form.is_valid():
            listing = Listing(
                title=form.cleaned_data['title'], 
                description=form.cleaned_data['description'], 
                img_url=form.cleaned_data['img_url'],
                starting_bid=form.cleaned_data['starting_bid'],
                max_bid=form.cleaned_data['starting_bid'],
                listed_by= request.user,
            )
        
            if form.cleaned_data['category']:
                listing.category = Category.objects.get(pk=int(form.cleaned_data['category']))

            listing.save()

            listing.watchers.add(request.user)

            request.session['count'] += 1

            return render(request, 'auctions/create_listing.html', {
                'form': CreateListingForm(),
                'message': {'data':'Listing added successfully!', 'color': 'alert-success'},
                'count': request.session['count'],
            })

        else: 
            return render(request, 'auctions/create_listing.html', {
                'form': CreateListingForm(),
                'message': {'data':'Something wrong happened!', 'color': 'alert-danger'},
                'count': request.session['count'],
            })

    return render(request, 'auctions/create_listing.html', {
        'form': CreateListingForm(),
        'count': request.session['count'],
    })

@login_required
def listing(request, id):

    listing = Listing.objects.get(pk=id)
    
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'in_watchlist': listing in request.user.watchlist.all(),
        'bidding_form': BiddingForm(),
        'comment_form': CommentForm(),
        'comments': listing.comments.order_by('-created_at'),
        'bids_count': listing.bids.count(),
        'count': request.session.get('count', None),
    }) 


@login_required
def watch(request, id):
    if request.method == 'POST':

        listing = Listing.objects.get(pk=id)
        watchers = listing.watchers
        user = request.user 

        if not user in watchers.all():
            watchers.add(user)
            request.session['count'] += 1

        else:
            watchers.remove(user)
            request.session['count'] -= 1

        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))


@login_required
def bid(request, id):
    if request.method == 'POST':

        form = BiddingForm(request.POST)
        listing = Listing.objects.get(pk=id)
        
        if form.is_valid() and listing.listed_by != request.user and not listing.closed:

            bid = form.cleaned_data['bid']

            if bid > listing.max_bid or (bid == listing.starting_bid and listing.bids.count() == 0): 
                bidding = Bid(
                    bid=bid,
                    listing=listing, 
                    bidder= request.user
                )

                bidding.save()

                listing.max_bid=bid
                listing.last_bidder=request.user

                listing.save()

            else: 
                return render(request, 'auctions/listing.html', {
                    'listing': listing,
                    'in_watchlist': listing in request.user.watchlist.all(),
                    'bidding_form': BiddingForm(),
                    'comment_form': CommentForm(),
                    'comments': listing.comments.order_by('-created_at'),
                    'bids_count': listing.bids.count(),
                    'count': request.session.get('count', None),
                    'message': {'data':'Your bid must be higher than the current bid', 'color': 'text-danger'},
                })

        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))


@login_required
def close(request, id):
    if request.method == 'POST' :

        listing = Listing.objects.get(pk=id)

        if listing.listed_by == request.user and not listing.closed:
            listing.closed = True
            listing.save()

    return HttpResponseRedirect(reverse('listing', args=(id,)))


@login_required
def comment(request):
    if request.method == 'POST':

        form = CommentForm(request.POST)
        listing = Listing.objects.get(pk=int(request.POST['listing']))

        if form.is_valid():

            comment = form.cleaned_data['comment']

            comment = Comment(
                comment=comment,
                listing=listing, 
                commented_by= request.user
            )

            comment.save()

        return HttpResponseRedirect(reverse('listing', args=(listing.id,)))


@login_required
def watchlist(request):

    return render(request, 'auctions/index.html', {
        'headline': 'Watchlist',
        'listings': request.user.watchlist.all()[::-1],
        'count': request.session['count']
    })


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            request.session['count'] = request.user.watchlist.count()

            if not request.POST.get('next'):
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponseRedirect(request.POST.get('next'))

        else:
            return render(request, 'auctions/login.html', {
                'message': 'Invalid username and/or password.',
            })
    else:
        return render(request, 'auctions/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'auctions/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'auctions/register.html', {
                'message': 'Username already taken.'
            })
            
        login(request, user)

        request.session['count'] = request.user.watchlist.count()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/register.html')
