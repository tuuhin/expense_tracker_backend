from typing import Optional, Any
from django.forms import ValidationError, ModelForm
from django.contrib.auth.models import User
from plans.models import Budget
from .models import Expenses, Income


class ExpenseForm(ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'

    def clean(self) -> Optional[dict[str, Any]]:
        errors: list[ValidationError] = []
        user: User = self.cleaned_data['user']
        title: str = self.cleaned_data['title']
        amount: float = self.cleaned_data['amount']
        budget: Budget = self.cleaned_data['budget']
        remaining_budget: float = budget.total_amount-budget.amount_used

        if not title.istitle():
            errors.append(ValidationError(
                {'title': "Should be of title case"}, code="invalid")
            )
        if remaining_budget > amount:
            errors.append(ValidationError(
                {'amount': f'Budget overflowed by {round(remaining_budget,2)}'}))

        if budget.user != user:
            errors.append(ValidationError(
                {"budget": "This budget dont belog to this user "})
            )

        if errors:
            raise ValidationError(*errors)
        return super().clean()


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = '__all__'

    def clean(self) -> Optional[dict[str, Any]]:
        title: str = self.cleaned_data['title']
        if not title.istitle():
            raise ValidationError({"title": "Should be of title case"})
        return super().clean()
