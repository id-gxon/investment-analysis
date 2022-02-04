from django.db import models
from django.contrib.auth.models import User
# from django.urls import reverse


class Discussion(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_discussion')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name="voter_discussion")

    def __str__(self):
        return self.subject
    #
    # def get_absolute_url(self):
    #     return reverse('board: discussion_detail', args=[str(self.id)])


class Answer(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    voter = models.ManyToManyField(User, related_name='voter_answer')
