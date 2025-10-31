from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from .models import Book, Comment


def dashboard(request):
    books = Book.objects.all()


    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)


    language = request.GET.get('language')
    if language and language != 'all':
        books = books.filter(language=language)

    context = {
        'books': books,
        'query': query or '',
        'selected_language': language or 'all'
    }
    return render(request, 'book/index.html', context)

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "Bunday email topilmadi!")
            return redirect("login_user")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect("dashboard")
        else:
            messages.error(request, "Email yoki parol xato!")
            return redirect("login_user")

    return render(request, 'book/login.html')

def register_user(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password != confirm_password:
            messages.error(request, "Parollar bir xil emas!")
            return redirect("register_user")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro‘yxatdan o‘tgan!")
            return redirect("register_user")

        username = email.split("@")[0]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = fullname
        user.save()

        messages.success(request, "Ro‘yxatdan o‘tish muvaffaqiyatli! Endi tizimga kiring.")
        return redirect("login_user")

    return render(request, 'book/register.html')




def about(request):
    return render(request, 'book/about.html')



def user_logout(request):
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz.")
    return redirect("login_user")


def reset_password(request):
    return render(request, "book/reset.html")



def toggle_like(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user.is_authenticated:
        if request.user in book.likes.all():
            book.likes.remove(request.user)
            liked = False
        else:
            book.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': book.total_likes()})
    return JsonResponse({'error': 'Login kerak!'}, status=403)




 
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    related_books = Book.objects.exclude(id=book.id)[:4]
    comments = book.comments.all().order_by("-created_at")

    if request.method == "POST":
        # Like bosish
        if "like" in request.POST:
            if request.user.is_authenticated:
                if request.user in book.likes.all():
                    book.likes.remove(request.user)
                else:
                    book.likes.add(request.user)
            return redirect("book_detail", pk=pk)

        
        if "comment" in request.POST:
            if request.user.is_authenticated:
                text = request.POST.get("text")
                if text.strip():
                    Comment.objects.create(book=book, user=request.user, text=text)
            return redirect("book_detail", pk=pk)

    context = {
        "book": book,
        "related_books": related_books,
        "comments": comments,
    }
    return render(request, "book/book_detail.html", context)