from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    LANGUAGE_CHOICES = [
        ('uzbek', "O'zbek"),
        ('russian', 'Rus'),
        ('english', 'Ingliz'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='uzbek')
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_books', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.book.title}"
