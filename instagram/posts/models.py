import string as str
from random import choice

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from accounts.models import User


def generate_id():
        n = 10
        random = str.ascii_uppercase + str.ascii_lowercase + str.digits
        return ''.join(choice(random) for _ in range(n))


@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(User, related_name='post')
    slug = models.SlugField(unique=True, max_length=10, default=generate_id)
    photo = models.FileField(upload_to='posts_photo')
    caption = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-date_created', ]

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('posts:view', kwargs={'slug': self.slug})


@python_2_unicode_compatible
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='like_post')
    user = models.ForeignKey(User, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.user, self.post)
