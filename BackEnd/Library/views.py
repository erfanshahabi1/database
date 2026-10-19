from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Book, Member, Borrow, Author, Publisher
from .forms import BorrowForm, FineForm, ReturnBookForm, AddBookForm

def home(request):
    return render(request, 'home.html')

def low_inventory_books(request):
    books = Book.objects.filter(inventory__lt=5)
    return render(request, 'low_inventory_books.html', {'books': books})

def member_borrowed_books(request):
    members = Member.objects.prefetch_related('borrow_set__book')
    return render(request, 'member_borrowed_books.html', {'members': members})

def lend_book(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save()
            member = borrow.member
            member.number_of_borrowed_books += 1
            member.save()
            book = borrow.book
            book.inventory -= 1
            book.save()
            return JsonResponse({'message': 'Book lent successfully'})
    else:
        form = BorrowForm()
    return render(request, 'lend_book.html', {'form': form})

def calculate_fine(request):
    if request.method == 'POST':
        form = FineForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return_date = form['return_date']
            due_date = form['due_date']
            fine = max((return_date - due_date).days * 1000, 0)
            return JsonResponse({'fine': fine})
    else:
        form = FineForm()
    return render(request, 'calculate_fine.html', {'form': form})

def return_book(request):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            borrow = get_object_or_404(Borrow, borrow_id=form['borrow_id'])
            borrow.book.inventory += 1
            borrow.member.borrowedbooknum -= 1
            borrow.delete()
    else:
        form = ReturnBookForm()
    return render(request, 'return_book.html', {'form': form})

def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            form.save()
            message = 'Book added successfully.'
            return JsonResponse({'message': message})
    else:
        form = AddBookForm()
    return render(request, 'add_book.html', {'form': form})
