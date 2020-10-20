from django.forms import ModelForm
from network.models import Post

class ComposePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']