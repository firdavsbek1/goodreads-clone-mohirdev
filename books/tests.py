from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_book_content(self):
        response=self.client.get(reverse('books:list'))

        self.assertContains(response,'No books found.')

    def test_books_created(self):
        book1=Book.objects.create(title='The Test1',isbn='34r49n3r8',description='Test description')
        book2=Book.objects.create(title='The Test2',isbn='34r49n3r8',description='Test description')
        book3=Book.objects.create(title='The Test3',isbn='34r49n3r8',description='Test description')

        response=self.client.get(reverse('books:list')+'?page_size=2')

        for book in [book1,book2]:
            self.assertContains(response,book.title)
        self.assertNotContains(response,book3.title)

        response=self.client.get(reverse('books:list')+'?page=2&page_size=2')
        self.assertContains(response,book3.title)

    def test_book_detail_page(self):
        Book.objects.create(title='The Test',isbn='34r49n3r8',description='Test description')

        book=Book.objects.get(title='The Test')

        response=self.client.get(reverse('books:detail',kwargs={'pk':book.id}))
        self.assertContains(response,book.title)
        self.assertContains(response,book.isbn)
        self.assertContains(response,book.description)

    def test_search_results(self):
        book1 = Book.objects.create(title='The Avengers', isbn='34r49n3r8', description='Test description')
        book2 = Book.objects.create(title='The Killing in pain', isbn='34r49n3r8', description='Test description')
        book3 = Book.objects.create(title='The Unique habit of rabbit', isbn='34r49n3r8', description='Test description')

        response=self.client.get(reverse('books:list')+"?q="+book1.title)
        self.assertContains(response,book1.title)
        self.assertNotContains(response,book2.title)
        self.assertNotContains(response,book3.title)

        response = self.client.get(reverse('books:list') + "?q=" + book2.title)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + "?q=" + book3.title)
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)


class BookReviewTestCase(TestCase):

    def test_review_created(self):
        book=Book.objects.create(title='The Test1', isbn='34r49n3r8', description='Test description')
        user = CustomUser.objects.create_user(
            username='test',
            first_name='Test',
            last_name="User",
            email='test@gmail.com',
            password='anypassword'
        )
        self.client.login(username='test', password='anypassword')
        response=self.client.post(
            reverse('books:add-review',args=[book.id]),
            data={
                'stars_given':4,
                'comment':'The worst case scenario book!'
            }
        )
        review=book.reviews.all()[0]
        self.assertEqual(book.reviews.count(),1)
        self.assertEqual(review.stars_given,4)
        self.assertEqual(review.comment,"The worst case scenario book!")
        self.assertEqual(review.user,user)
        self.assertEqual(review.book,book)

        response = self.client.post(
            reverse('books:add-review', args=[book.id]),
            data={
                'stars_given': 10,
                'comment': 'Very like it though'
            }
        )

        self.assertFormError(response,'form','stars_given','Ensure this value is less than or equal to 5.')


