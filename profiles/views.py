from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserProfileForm
from .models import UserProfile
from checkout.models import Order


@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')

    else:
        form = UserProfileForm(instance=profile)

    orders = Order.objects.filter(email=request.user.email).order_by('-date')

    context = {
        'form': form,
        'orders': orders,
    }

    return render(request, 'profiles/profile.html', context)