from django.urls import path
from .views import base_information
from .views_income import income_details, income, update_sources, sources
from .views_expense import expenses, upgrade_categories, categories
from .multimodelviews import Entries

urlpatterns = [

    path('info', base_information, name="base_info"),
    path('sources', sources, name="sources"),
    path('sources/<int:pk>', update_sources, name='update_sources'),
    path('catergory/<int:pk>', upgrade_categories, name="upgrade_categories"),
    path('income', income, name='income'),
    path('income/<int:pk>', income_details, name="income_details"),
    path('categories', categories, name='categories'),
    path('expenses', expenses, name="expenses"),
    path('entries', Entries.as_view(), name="entries"),

]
