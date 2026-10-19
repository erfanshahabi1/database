from django.db import models
from django.utils import timezone

class Publisher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    publisher_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    author_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employee_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_employment = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Manager(Employee):
    pass

class Librarian(Employee):
    pass

class Cleaner(Employee):
    pass

class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, primary_key=True)
    # book_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField()
    description = models.TextField()
    year_of_publication = models.IntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ManyToManyField(Author)

    def __str__(self):
        return f"{self.title}"

class Historical(Book):
    pass

class Cultural(Book):
    pass

class Specialized(Book):
    pass

class Story(Book):
    pass

class Member(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    memberid = models.AutoField(primary_key=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    borrowedbooknum = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"

class MembershipStatus(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    membership_date = models.DateField()
    expiration_date = models.DateField()

class Borrow(models.Model):
    borrow_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"(member: {self.member}), (book: {self.book}), (borrow_id: {self.borrow_id})"
