from django.contrib import admin
from .models import Income,  Source, Category, Expenses


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('user',)


@admin.register(Expenses)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "amount", "added_at")
    ordering = ("-added_at",)
    list_filter = ('user',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'added_at')
    ordering = ('-added_at',)
    list_filter = ('user',)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_secure')
    list_filter = ('user',)
