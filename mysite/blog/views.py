from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Post, LikeDislike
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

# View for blog list
def blog_list(request):
    blog_list = Post.objects.all()  # Query the Post model
    return render(request, 'blog/blog_list.html', {'blog_list': blog_list})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if post.liked_users.filter(id=user.id).exists():
        # If the user already liked the post, remove the like
        post.liked_users.remove(user)
    else:
        # Add a like and remove a dislike if it exists
        post.liked_users.add(user)
        post.disliked_users.remove(user)  # Remove dislike

    return JsonResponse({
        'likes_count': post.likes_count(),
        'dislikes_count': post.dislikes_count()
    })


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if post.disliked_users.filter(id=user.id).exists():
        # If the user already disliked the post, remove the dislike
        post.disliked_users.remove(user)
    else:
        # Add a dislike and remove a like if it exists
        post.disliked_users.add(user)
        post.liked_users.remove(user)  # Remove like

    return JsonResponse({
        'likes_count': post.likes_count(),
        'dislikes_count': post.dislikes_count()
    })


# View for creating a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Handling file uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'form_type': 'Create'})


# View for updating an existing post
@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        print("FILES:", request.FILES)  # Debugging output
        print("POST:", request.POST)    # Debugging output
        
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            print("Post updated successfully.")  # Debugging confirmation
            return redirect('blog_list')
        else:
            print("Form errors:", form.errors)  # Debugging errors
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/blog_form.html', {'form': form, 'form_type': 'Edit'})


# View for deleting a post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('blog_list')  # Redirect to the blog list after deletion

# View for the "About" page
def about(request):
    return render(request, 'blog/about.html')

# View for blog post details
def blog_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the user has liked or disliked the post
    if request.user.is_authenticated:
        user_like_dislike = LikeDislike.objects.filter(user=request.user, post=post).first()
        has_liked = user_like_dislike.is_like if user_like_dislike else False
        has_disliked = not has_liked if user_like_dislike else False
    else:
        has_liked = has_disliked = False

    return render(request, 'blog/blog_details.html', {
        'post': post,
        'has_liked': has_liked,
        'has_disliked': has_disliked,
        'likes_count': post.likes_count(),
        'dislikes_count': post.dislikes_count(),
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to the login page (update the name if needed)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

#API Views

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Post, LikeDislike
from .serializers import PostSerializer, LikeDislikeSerializer

# View for listing and creating posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# View for retrieving, updating, and deleting a post
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# View for liking/disliking a post
class LikeDislikeCreateView(generics.CreateAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        is_like = request.data.get('is_like', None)

        if is_like is None:
            return Response({'error': 'is_like is required'}, status=status.HTTP_400_BAD_REQUEST)

        like_dislike, created = LikeDislike.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'is_like': is_like}
        )

        # Update the `liked_users` and `disliked_users` ManyToMany relationships
        if is_like:
            post.liked_users.add(request.user)
            post.disliked_users.remove(request.user)
        else:
            post.disliked_users.add(request.user)
            post.liked_users.remove(request.user)

        return Response({
            'likes_count': post.likes_count(),
            'dislikes_count': post.dislikes_count(),
        }, status=status.HTTP_200_OK)
