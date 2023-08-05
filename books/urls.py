from django.urls import path
import books.views as views


app_name='books'
urlpatterns=[
    path('',views.BookListView.as_view(),name='list'),
    path('<int:pk>/',views.BookDetailView.as_view(),name='detail'),
    path('<int:pk>/reviews/create/',views.AddReviewView.as_view(),name='add-review'),
    path('<int:book_id>/reviews/<int:review_id>/edit/',views.EditReviewView.as_view(),name='edit-review'),
    path('<int:book_id>/reviews/<int:review_id>/delete/',views.DeleteReviewView.as_view(),name='delete-review'),
]