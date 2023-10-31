from django.shortcuts import render, redirect, get_object_or_404
from .models import Posting, Comment
from .forms import PostingForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

def index(request):
    return render(request, 'postings/index.html')

def posting_list(request):
    postings = Posting.objects.order_by('date').reverse()
    postings_num = postings.count()
    if postings_num == 0:
        context = {
            'postings_num': postings_num,
            'move_previous': False,
            'move_next': False,
            'page_range': [1],
            'page_postings': None,
        }
        return render(request, 'postings/posting_list.html', context)

    paginator = Paginator(postings, 10)

    page = request.GET.get('page')
    if page == None:
        page = '1'
    elif page == '0' or not page.isdecimal():
        return render(request, '404.html')

    count = 5
    recent_page = int(page)
    
    last_page = postings_num // 10
    if postings_num % 10 != 0:
        last_page += 1
    if recent_page > last_page:
        return render(request, '404.html')
    
    previous_page = ((recent_page-1)//count)*count
    move_previous = True
    if previous_page < count:
        move_previous = False
    
    next_page = ((recent_page-1)//count+1)*count+1
    move_next = True
    if next_page > last_page:
        move_next = False
    
    start_page = previous_page+1
    end_page = next_page-1
    if end_page > last_page:
        end_page = last_page

    page_range = list(range(start_page, end_page+1))
    page_postings = paginator.get_page(page)

    page_postings_start_index = postings_num-(recent_page-1)*10

    context = {
        'postings_num': postings_num,
        'last_page': last_page,
        'previous_page': previous_page,
        'move_previous': move_previous,
        'next_page': next_page,
        'move_next': move_next,
        'page_range': page_range,
        'page_postings': page_postings,
        'page_postings_start_index': page_postings_start_index,
    }
    return render(request, 'postings/posting_list.html', context)

def posting_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            posting_form = PostingForm(request.POST)
            
            if posting_form.is_valid():
                posting_form = posting_form.save(commit=False)
                posting_form.author = request.user
                posting_form.save()
                return redirect('postings:posting_list')
        else:
            posting_form = PostingForm()
        
        context = {
            'posting_type': '글쓰기',
            'posting_form': posting_form,
        }
        return render(request, 'postings/posting_form.html', context)
    return redirect('accounts:login')

def posting_detail(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.posting = posting
            comment_form.author = request.user
            comment_form.save()
            return redirect('postings:posting_detail', posting_id)
    else :
        comment_form = CommentForm()
    
    comments = posting.comment_list.all()

    context = {
        'posting': posting,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'postings/posting_detail.html', context)

@login_required
def posting_update(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    if posting.author == request.user:
        if request.method == 'POST':
            posting_form = PostingForm(request.POST, instance=posting)

            if posting_form.is_valid():
                posting_form.save()
                return redirect('postings:posting_detail', posting_id)
        else:
            posting_form = PostingForm(instance=posting)

        context = {
            'posting_type': '글수정',
            'posting': posting,
            'posting_form': posting_form,
        }
        return render(request, 'postings/posting_form.html', context)
    return redirect('postings:posting_detail', posting_id)

@login_required
@require_POST
def posting_delete(request, posting_id):
    posting = get_object_or_404(Posting, id=posting_id)
    if posting.author == request.user:
        posting.delete()
        return redirect('postings:posting_list')
    return redirect('postings:posting_detail', posting_id)

@login_required
@require_POST
def comment_delete(request, posting_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('postings:posting_detail', posting_id)
