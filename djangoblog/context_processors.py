
from .forms import SearchForm

def search_form(request):
    return {'global_search_form': SearchForm()}
