from django.shortcuts import render


def community_home(request):
    return render(request, 'community/community_home.html')