from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    full_text = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class GlossaryTerm(models.Model):
    term = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, default='Теория')
    definition = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.term

class Vacancy(models.Model):
    position = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.position

class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()

    def __str__(self):
        return self.question

class CompanyContact(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class CompanyHistory(models.Model):
    year = models.PositiveIntegerField()
    event = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.year} — {self.event[:30]}"