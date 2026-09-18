from django.shortcuts import render # type: ignore

# Create your views here.

# substituído pelo pacote views (pasta views)
def index (request):
    return render(
        request, 'contact/index.html'
    )