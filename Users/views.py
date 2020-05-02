from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid:
			try:
				form.save()
				return redirect("/check")
			except:
				pass
	else:
		form = UserCreationForm()
	return render(request, "register.html", {'form': form})

def homepage(request):
	return render(request, "home.html")

