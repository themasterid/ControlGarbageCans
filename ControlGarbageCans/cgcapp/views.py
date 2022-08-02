from django.shortcuts import render
from geopy.geocoders import Nominatim


def index(request):
    # print(request.GET.get('demo'))
    geoLoc = Nominatim(user_agent="GetLoc")
    # 56.85309060825822, 35.90764498656374
    location_name = geoLoc.reverse("56.85309060825822, 35.90764498656374")
    address = location_name.address
    print(address.split(', '))
    context = {
        'address': address.split(', ')}
    return render(
        request,
        'cgcapp/index.html',
        context)
