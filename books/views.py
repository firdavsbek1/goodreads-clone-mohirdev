from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from books.forms import ReviewForm
from books.models import Book, Review
from django.core.exceptions import PermissionDenied


class BookListView(View):
    def get(self,request):
        books=Book.objects.all().order_by('id')

        # search
        search_query=request.GET.get('q','')
        books=books.filter(title__icontains=search_query)

        # pagination
        paginator=Paginator(books,request.GET.get('page_size',4))
        page_number=request.GET.get('page',1)
        page_obj=paginator.get_page(page_number)

        return render(request,'books/list.html',{'page_obj':page_obj,'search_query':search_query})


# class BookListView(generic.ListView):
#     queryset = Book.objects.all()
#     template_name = 'books/list.html'
#     context_object_name = 'books'
#     paginate_by = 2


class BookDetailView(View):
    def get(self,request,pk):
        book=Book.objects.get(id=pk)
        form=ReviewForm()
        return render(request,'books/detail.html',{'book':book,'form':form})


class AddReviewView(LoginRequiredMixin,View):

    def post(self,request,pk):
        book=get_object_or_404(Book,id=pk)
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.book=book
            review.user=request.user
            review.save()
            return redirect(reverse('books:detail',args=[book.id]))
        return render(request,'books/detail.html',{'book':book,'form':form})


class EditReviewView(LoginRequiredMixin,View):
    def get(self,request,book_id,review_id):
        review=Review.objects.get(id=review_id)
        form=ReviewForm(instance=review)
        if review.user == request.user:
            return render(request,'books/edit-review.html',context={"form":form,'review':review})
        raise PermissionDenied()

    def post(self,request,book_id,review_id):
        review=Review.objects.get(id=review_id)
        form=ReviewForm(instance=review,data=request.POST)
        if review.user==request.user:
            if form.is_valid():
                form.save()
                messages.info(request,"You have successfully edited your comment.")
                return redirect(reverse('books:detail', args=[book_id]))
        raise PermissionDenied()


class DeleteReviewView(LoginRequiredMixin,View):
    def get(self,request,book_id,review_id):
        review=Review.objects.get(id=review_id)
        book=Book.objects.get(id=book_id)
        return render(request,'books/delete-review.html',{'review':review,'book':book})

    def post(self,request,book_id,review_id):
        review=Review.objects.get(id=review_id)
        review.delete()
        messages.success(request,'You have successfully deleted your comment.')
        return redirect(reverse('books:detail',args=[book_id]))



