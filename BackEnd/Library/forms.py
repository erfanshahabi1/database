from django import forms
from .models import Book, Borrow

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['member', 'book', 'borrow_date', 'due_date']

class FineForm(forms.Form):
    return_date = forms.DateField()
    due_date = forms.DateField()

class ReturnBookForm(forms.Form):
    borrow_id = forms.CharField()

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'inventory', 'description', 'year_of_publication', 'publisher', 'author']
