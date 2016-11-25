from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib import auth

from lab.models import Tutor, Course
from lab.forms import SignupForm, SigninForm


def main(request):
    tutors = Tutor.objects.all()

    return render(request, 'main.html', {
        'tutors': tutors
    })


def signup(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(redirect)
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form
    })


def signin(request):
    redirect = request.GET.get('continue', '/success')
    if request.method == "POST":
        form = SigninForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = SigninForm()
    return render(request, 'signin.html', {
        'form': form
    })


@login_required(redirect_field_name='continue')
def login_success(request):
    return render(request, 'success.html')


def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)


class TutorView(View):
    def get(self, request, id):
        tutor = Tutor.objects.get(id=int(id))

        courses = Course.objects.filter(tutor=tutor).all()

        return render(request, 'tutor.html', {
            'tutor': tutor,
            'courses': courses
        })
