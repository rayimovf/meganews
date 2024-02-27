from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=70)
    img = models.ImageField(upload_to='CategoryIMG')

    def __str__(self):
        return self.name


class Banner(models.Model):
    img = models.ImageField(upload_to='BannerIMG')
    title = models.CharField(max_length=255)
    text = models.TextField()


class Profile(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    banner = models.ImageField(upload_to='ProfileBannerIMG', null=True, blank=True)
    explanation = models.TextField()
    img = models.ImageField(upload_to='ProfileIMG', null=True, blank=True)

    def __str__(self):
        return self.first_name


class About(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    videos = models.FileField(upload_to='AboutVideo')


class Information(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=25)
    fax = models.CharField(max_length=70)
    address = models.CharField(max_length=255)
    instagram = models.CharField(max_length=70)
    twitter = models.CharField(max_length=70)


class Team(models.Model):
    img = models.ImageField(upload_to='TeamIMG')
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Contact(models.Model):
    subject = models.CharField(max_length=255)
    name = models.CharField(max_length=70)
    email = models.EmailField()
    explanation = models.TextField()
    file = models.FileField(upload_to='Contact', null=True, blank=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    img = models.ImageField(upload_to='PostIMG')
    date = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    viewed = models.IntegerField(default=0)


class PostVideos(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tags)
    video = models.URLField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)


class SavedPost(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post)

