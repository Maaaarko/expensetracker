from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExpenseListView.as_view(), name="expenses"),
    path("<int:id>", views.ExpenseView.as_view(), name="expense"),
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("categories/<int:id>", views.CategoryView.as_view(), name="category"),
]