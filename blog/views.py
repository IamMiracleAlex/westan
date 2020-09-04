from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Subscribe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib import messages


def blog_index(request, tag_slug=None):
    object_list = Post.objects.filter(published=True)
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6) # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an intger deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #  if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'posts': posts,
                                                'page': page, 'tag': tag})
                                              'page': page, 'tag': tag})




def blog_single(request, pk, slug):
    # post = get_object_or_404(Post, slug=slug, pk=pk)
    post = get_object_or_404(Post, pk=pk)

    # list of active comments for this post
    comments = post.comment_set.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create from object but don't save to the db
            new_comment = comment_form.save(commit=False)
            new_comment.post = post # assign current post to the comment
            new_comment.save() # save comment to db
        
            # comment_form = CommentForm()
    else:
        comment_form = CommentForm()


    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)

    similar_posts = Post.objects.filter(published=True).filter(
                                        tags__in=post_tags_ids).exclude(id=post.id)

    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by(
                                        '-same_tags',)[:4]
        
    return render(request, 'blog/blog_single.html', {'post':post, 'comments': comments,
                                                'new_comment': new_comment, 'comment_form': comment_form,
                                                'similar_posts': similar_posts})

                                              'similar_posts': similar_posts})



                                                

def search(request):
    results = []
    query = None
    
    if 'query' in request.GET:
        query = request.GET['query']

        results = Post.objects.filter(title__icontains=query)
    return render(request, 'blog/search.html', {'query': query,
                                            'results': results})
