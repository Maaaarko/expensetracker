from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("auth.urls")),
    path("expenses/", include("expenses.urls")),
    path("social/", include("social.urls"))

]
