from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize
from django.db.models import Model, ForeignKey, CharField, DateTimeField, ManyToManyField, CASCADE


class User(AbstractUser):
    pass
    
class Post(Model):
    author = ForeignKey(User, on_delete=CASCADE, related_name='posts')
    content = CharField(max_length = 256)
    timestamp = DateTimeField(auto_now_add=True)
    liked_by = ManyToManyField(User, blank=True, related_name='liked_posts')

    def serialize_post(self):
        return {'id': self.id, 'author': self.author.username, 'content':self.content, 'timestamp': self.timestamp}

class Follow(Model):
    follower = ForeignKey(User, on_delete=CASCADE, related_name='following_users')
    following = ForeignKey(User, on_delete=CASCADE, related_name='followed_users')

