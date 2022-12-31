from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.models import User, Bid, Category, Listing, Watchlist, Comment




from .forms import ListingForm


def index(request):
    all_listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        'all_listings':all_listings
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

def create_listing(request):
    if request.method == 'POST':
        import datetime
        listing_form = ListingForm(request.POST, request.FILES)
        if listing_form.is_valid():
            bid = listing_form.cleaned_data['starting_bid']
            print(bid)
            listing = listing_form.save(commit=False)
            listing.user = request.user
            print(listing.user)
            listing.date_made = datetime.datetime.today()
            listing.is_active = True
            listing.category = Category.objects.get(name=listing_form.cleaned_data['listing_category'])
            print(listing.category)
            #The form is being saved correctly here, and the print statements give the correct results in my terminal
            listing.save()
            Bid.objects.create(user= request.user, value=bid, listing=listing_form.instance)
            all_listings = Listing.objects.all()
            return render(request, 'auctions/index.html', {
                'all_listings': all_listings })
        
    else:
        listing_form = ListingForm()
        return render(request, 'auctions/createlisting.html',{
        'listing_form':listing_form
    })

def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    #the print results return the default values for the fields category and user instead of the values I saved in my ModelForm
 
    last_bid = listing.bids.last()
    bid_winner = last_bid.user
    comments = Comment.objects.all()
    if request.user == listing.user:
        if bid_winner == request.user:
            return render(request, 'auctions/view_listing.html',{
                'listing': listing,
                'bid_winner': bid_winner,
                'count': (listing.bids.all().count() - 1),
                'comments':comments,
                'flag':True
            })
        
        
        else:
            return render(request, 'auctions/view_listing.html', {
                'listing': listing,
                'comments':comments,
                'count': (listing.bids.all().count() - 1),
                'flag':True})

    else:
        if bid_winner == request.user:

            return render(request, 'auctions/view_listing.html',{
                'listing':listing,
                'bid_winner':bid_winner,
                'count': (listing.bids.all().count() - 1),
                'comments':comments})
        else:
            return render(request, 'auctions/view_listing.html', {
                'listing':listing,
                'count': (listing.bids.all().count() - 1),
                'comments':comments})

            
        



def add_to_watchlist(request, listing_id):
    #check to see if user is logged in
    if not request.user.is_authenticated:
        #return user to login page if theyre not logged in
        return HttpResponseRedirect(reverse('login'))
    else:
        # get watchlist if one already exists, if the watchlist does not exist, create a new watchlist
        watchlist, created = Watchlist.objects.get_or_create(user = request.user)
        try:
            # check to see if a listing with the given listing_id exists
            watchlist.listings.get(pk=listing_id)
            #return a page to tell the user that the listing is already part of the watchlists
            return render(request, 'auctions/watchlist.html', {
                'listings': watchlist.listings.all(),
                'message': 'The listing is already a part of your watchlist'
                
            })
        except:
            #if the listing is not part of the watchlist, get the watchlist from the model Listing
            listing = Listing.objects.get(id= listing_id)
            #add listing to watchlist
            watchlist.listings.add(listing)
            # return a page showing the user all the listings in their watchlist
            return render(request, 'auctions/watchlist.html', {
                'listings': watchlist.listings.all()
            })

def view_watchlist(request):
    #check to see if the user is logged in.
    if not request.user.is_authenticated:
        #if not logged in redirect user to login page.
        return HttpResponseRedirect(reverse('login'))
    #if user is loggged in.
    else:
        
        try:
            # attempt to get a watchlist specific to the user
            watchlist = Watchlist.objects.get(user = request.user)
            return render(request, 'auctions/watchlist.html',{
                # display a watchlist page with all the users listings.
                "listings":watchlist.listings.all()
            })
        except:# user does not have a watchlist specific to them.
            return render(request, 'auctions/index.html',{
                # redirect the user to the main page but with a message on top
                'message':"You haven't added any items to your watchlist yet"
            })

def remove_from_watchlist(request, listing_id):
    watchlist = Watchlist.objects.get(user = request.user)
    listing = Listing.objects.get(pk=listing_id)
    watchlist.listings.remove(listing)
    
    return render(request, 'auctions/watchlist.html',{
        'listings': watchlist.listings.all(),
        'message':'The listing has been deleted successfully!'
    })
def bid(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk = listing_id)
        bid = request.POST['bid']
        if float(bid) <= listing.starting_bid:
            return render(request, 'auctions/view_listing.html', {
                'listing':listing,
                'message': 'Your bid must be greater than the current bid!'              
            })
        else:
            listing.starting_bid = bid
            listing.save()
            bid_instance = Bid(user=request.user, value=bid, listing=listing)
            
            bid_instance.user = request.user
            bid_instance.save()

            
           
            comments = Comment.objects.all()
            
            if request.user == listing.user:
                return render(request, 'auctions/view_listing.html',{
                    'listing':listing,
                    'count': (listing.bids.all().count() - 1),
                    'comments':comments,
                    'flag':True
                    
                })
            else:
                return render(request, 'auctions/view_listing.html', {
                    'listing':listing,
                    'count': (listing.bids.all().count() - 1),
                    'comments':comments

                    
                })
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    listing.is_active = False
    listing.save()
    last_bid = listing.bids.last()
    bid_winner = last_bid.user
    
    
    comments = Comment.objects.all()
    if bid_winner==request.user:
        return render(request, 'auctions/view_listing.html', {
            'listing': listing,
            'bid_winner': bid_winner,
            'count': (listing.bids.all().count() - 1),
            'comments':comments
        })
    else:
        return render(request, 'auctions/view_listing.html', {
            'listing': listing,
            'count': (listing.bids.all().count() - 1)
        })

def add_comment(request, listing_id):
        
    if request.method == "POST":
        comment = Comment(user = request.user, comment_text= request.POST['comment_text'], listing = Listing.objects.get(pk=listing_id))
        comment.save()
        comments = Comment.objects.all()
        listing =  Listing.objects.get(pk=listing_id)
        last_bid = listing.bids.last()
        bid_winner = last_bid.user
        if request.user == listing.user:
            if bid_winner == request.user:
                return render(request, 'auctions/view_listing.html', {
                    'listing': listing,
                    'bid_winner': bid_winner,
                    'count': (listing.bids.all().count() - 1),
                    'comments':comments,
                    'flag':True})
            else:
            
                return render(request, 'auctions/view_listing.html', {
                'listing': listing,
                'count': (listing.bids.all().count() - 1),
                'comments':comments,
                'flag':True})
        else:
            
             if bid_winner == request.user:
                    return render(request, 'auctions/view_listing.html', {
                    'listing': listing,
                    'bid_winner': bid_winner,
                    'count': (listing.bids.all().count() - 1),
                    'comments':comments,})
                    
    else:
        if request.user == listing.user:    
                return render(request, 'auctions/view_listing.html', {
                'listing': listing,
                'count': (listing.bids.all().count() - 1),
                'comments':comments})
                

            
        
    
        comments = Comment.objects.all()
        if bid_winner == request.user:
            return render(request, 'auction/view_listing.html',{
                'comments':comments,
                'listing': listing,
                'bid_winner': bid_winner,
                'count': (listing.bids.all().count() - 1)})
        else:
            return render(request, 'auction/view_listing.html',{
                'comments':comments,
                'listing': listing,
                'count': (listing.bids.all().count() - 1)})
        

    








        



        
        
        

      

        
        


    
        
           



   
        








