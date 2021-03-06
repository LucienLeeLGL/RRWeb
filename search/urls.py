from django.urls import path
from search.views import *

app_name = "search"
urlpatterns = (
    path('result', search_result, name='result'),
    path('suggest', SearchSuggest.as_view(), name='suggest'),
    path('suggest_city', CityAddressSuggest.as_view(), name='suggest_city'),
    path('', SearchView.as_view(), name='search'),
)
