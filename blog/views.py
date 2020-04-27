from django.shortcuts import render, redirect
from .models import Post, BlogComment
from django.contrib import messages
# from django.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post':post, 'comments':comments, 'user':request.user, 'replyDict': replyDict} 
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully.")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            comment.save()
            messages.success(request, "Your reply has been posted successfully.")

    return redirect(f'/blog/{post.slug}') 



# GATE_NOTES
def gateNote(request):
    allPosts = Post.objects.all()
    # print(post)
    context = {'allPosts':allPosts} 
    return render(request, 'blog/gate/gateNote.html', context)

# YEAR-WISE PAPERS
def yearPaper(request):
    allPosts = Post.objects.all()
    # print(post)
    context = {'allPosts':allPosts} 
    return render(request, 'blog/gate/yearPaper.html', context)

def Y_2020(request):
    allPosts = Post.objects.all()
    # print(post)
    context = {'allPosts':allPosts} 
    return render(request, 'blog/gate/year/Y_2020.html', context)


# SUBJECT_WISE PAPERS
def subPaper(request):
    allPosts = Post.objects.all()
    # print(post)
    context = {'allPosts':allPosts} 
    return render(request, 'blog/gate/subPaper.html', context)

