from datetime import datetime, timedelta

from django.db import models
from django.utils.text import slugify
from django.utils.functional import cached_property


class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()
    client = models.CharField(max_length=100, blank=True)
    due_date = models.DateField(default=(datetime.today() + timedelta(days=14)))
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    @cached_property
    def budget_left(self):
        total_expense_amount = sum([expense.amount for expense in self.expenses.all()])
        return self.budget - total_expense_amount

    @cached_property
    def total_transactions(self):
        return len(self.expenses.all())

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("due_date", "name")


class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-amount",)
