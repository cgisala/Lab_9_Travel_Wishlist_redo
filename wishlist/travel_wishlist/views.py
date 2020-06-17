from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Controllers in an MVC architecture are called views in Django

@login_required
def place_list(request):

    """If this is a POST request, the user clicked the Add button
    in the form.  Check if the place is valid, if so, save a 
    new Place to the database, and redirect to this same page.
    This creates a GET request to this same route

    If not a POST route, or Place is not valid, display a page with 
    a list of places and a form to add a new place
    """

    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)     #Create a new Place from the form
        place.user = request.user   #Associate the place with the logged-in user
        if form.is_valid():     #Checks against DB constraints, for example, are required fields present?
            place.save()        #Saves to the database
            return redirect('place_list')       #redirects to GET view with name place_list - which is the same view

    #   If not a POST, or the form is not valid, render the page
    #   with the form to add a new place, and list of places
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name') #Fetches not visited places from the database
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})

@login_required
def place_was_visited(request, place_pk):

    # If this is a POST request, find the place with this pk, change visited to True,
    # and save
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)  # Gets the object or shows 404 if the PK is not in the database
        if place.user ==request.user:   #Only let user visit their own places
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
        
    # Redirect to place_list to show the wishlist
    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    #Checks to make sure the user who owns this place is 
    # the one editing it
    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        #instance is the model object to update with the form data

        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)    #Temp error message

        return redirect('place_details', place_pk=place_pk)

    else:   #Get place details
        if place.visited:
            review_form = TripReviewForm(instance=place)    #Pre-populate with data from this Place instance
            return render(request,  'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()