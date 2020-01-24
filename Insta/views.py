from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from Insta.models import Post, Like, InstaUser, UserConnection, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from Insta.forms import CustomUserCreationForm

class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'
    login_url = 'login'

class PostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    login_url = 'login'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = self.request.user
            following = set()
            for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
                following.add(conn.following)
            return Post.objects.filter(author__in=following)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
        if liked:
            data['liked'] = 1
        else:
            data['liked'] = 0
        return data

class UserDetailView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    login_url = 'login'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    template_name = 'post_create.html'
    fields = ['title', 'caption', 'picture']
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'caption']
    login_url = 'login'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
    login_url = 'login'

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

class EditProfile(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'edit_profile.html'
    fields = ['nickname']
    login_url = 'login'

class ExploreView(ListView):
    model = Post
    template_name = 'explore.html'

class UsersView(LoginRequiredMixin, ListView):
    model = InstaUser
    template_name = 'users_view.html'
    login_url = 'login'

class FollowingView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'following_view.html'
    login_url = 'login'

class FollowedView(LoginRequiredMixin, DetailView):
    model = InstaUser
    template_name = 'followed_view.html'
    login_url = 'login'

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('posts')

class PicUpdateView(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'pic_update.html'
    fields = ['profile_pic']
    login_url = 'login'

class FollowMyself(LoginRequiredMixin, CreateView):
    model = UserConnection
    template_name = 'follow_me.html'
    fields = []

    def form_valid(self, form):
        form.instance.creator = self.request.user
        fomr.instance.following = self.request.user
        return super().form_valid(form)
    

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 2
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }