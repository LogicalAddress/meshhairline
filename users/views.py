from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CustomUserProfileForm
from .models import User
from django.http import HttpResponseRedirect

@login_required
def index(request):
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, instance=User.objects.get(pk=request.user.pk))
        if form.is_valid():
            form.save(commit=True)
        else:
            return HttpResponseRedirect('/user/profile')
    form = CustomUserProfileForm(instance=User.objects.get(pk=request.user.pk))
    context = {
        'form': form,
    }
    return render(request, 'users/profile.html', context)
    