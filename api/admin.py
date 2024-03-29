from django.contrib import admin
from .models import Income,  Source, Category, Expenses
from .forms import ExpenseForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('user',)


@admin.register(Expenses)
class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseForm
    list_display = ("title", "user", "amount", "added_at")
    ordering = ("-added_at",)
    list_filter = ('user',)
    search_fields = ('user__username',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'added_at')
    ordering = ('-added_at',)
    list_filter = ('user',)
    search_fields = ('user__username',)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_secure')
    list_filter = ('user',)
