import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views.generic import CreateView

from .forms import ExpenseForm
from .models import Category, Expense, Project


def project_list(request):
    project = Project.objects.all()
    context = {"project_list": project}
    return render(request, "budget/project-list.html", context)


def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    if request.method == "GET":
        category_list = Category.objects.all()
        context = {
            "project": project,
            "expense_list": project.expenses.all(),
            "category_list": category_list,
        }
        return render(request, "budget/project-detail.html", context)

    elif request.method == "POST":

        project_id = json.loads(request.body).get("project_id")
        if project_id:
            # toggles project completion
            project.completed = not project.completed
            project.save()

            return HttpResponse("")

        form = ExpenseForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            amount = form.cleaned_data["amount"]
            category_name = form.cleaned_data["category"]

            category = get_object_or_404(Category, project=project, name=category_name)
            Expense.objects.create(
                project=project, title=title, amount=amount, category=category
            ).save()

    elif request.method == "DELETE":
        id = json.loads(request.body)["id"]
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse("")

    return HttpResponseRedirect(project_slug)


class ProjectCreateView(CreateView):
    model = Project
    template_name = "budget/add-project.html"
    fields = ("name", "client", "budget", "due_date")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST["categoriesString"].split(",")
        for category in categories:
            Category.objects.create(
                project=Project.objects.get(id=self.object.id), name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST["name"])
