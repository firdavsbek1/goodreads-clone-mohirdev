from django.test import TestCase
from django.urls import reverse

from books.models import Book, Review
from users.models import CustomUser


class HomePageReviewListTestCase(TestCase):
    def test_review_pagination(self):
        book = Book.objects.create(title='The Test1', isbn='34r49n3r8', description='Test description')
        user = CustomUser.objects.create_user(username='test', first_name='Test', last_name="User",
                                              email='test@gmail.com',
                                              password='anypassword'
                                              )
        review1=Review.objects.create(user=user,book=book,stars_given=5,comment='Amazing delusional book')
        review2=Review.objects.create(user=user,book=book,stars_given=5,comment='Very good')
        review3=Review.objects.create(user=user,book=book,stars_given=5,comment='I don\'t think it worth reading.')

        response=self.client.get(reverse('home_page')+"?page_size=1")

        self.assertContains(response,review1.comment)
        self.assertNotContains(response,review2.comment)
        self.assertNotContains(response,review3.comment)

        response = self.client.get(reverse('home_page') + "?page_size=1&page=2")

        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
        self.assertNotContains(response, review3.comment)
