from django.urls import path
from .views import base_information
from .views_income import (update_income, income, update_sources, sources)
from .views_expense import (
    expenses, upgrade_categories, categories, upgrade_expense)
from .multimodelviews import Entries

urlpatterns = [

    path('info', base_information, name="base_info"),
    path('sources', sources, name="sources"),
    path('sources/<int:pk>', update_sources, name='update_sources'),
    path('income', income, name='income'),
    path('income/<int:pk>', update_income, name="income_details"),
    path('categories', categories, name='categories'),
    path('categories/<int:pk>', upgrade_categories, name="upgrade_categories"),
    path('expenses', expenses, name="expenses"),
    path('expenses/<int:pk>', upgrade_expense, name="update-expenses"),
    path('entries', Entries.as_view(), name="entries"),

]
