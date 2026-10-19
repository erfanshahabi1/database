from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("Lows/", views.low_inventory_books, name="lows"),
    path("Books/", views.member_borrowed_books, name="books"),
    path("Lend/", views.lend_book, name="lend"),
    path("Fine/", views.calculate_fine, name="fine"),
    path("Return/", views.return_book, name="return"),
    path("Add/", views.add_book, name="add")
]
