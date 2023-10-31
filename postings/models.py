from django.db import models
from django.conf import settings

class Posting(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='postings')
    def __str__(self):
        posting_title = self.title
        if len(posting_title) > 10:
            posting_title = self.title[:10] + '...'
        return f'{posting_title} - 작성자:{self.author.username}'

class Comment(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name='comment_list')
    content = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
        comment_content = self.content
        if len(comment_content) > 10:
            comment_content = self.content[:10] + '...'
        return f'{comment_content} - 작성자:{self.author.username}'
