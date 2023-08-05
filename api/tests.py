from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, Review
from users.models import CustomUser


class ReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='firdavs',
            first_name='Firdavs',
            last_name="Jalolov",
            email='firddavs@gmail.com',
            password='anypassword'
        )
        self.client.login(username='firdavs',password='anypassword')

    def test_review_detail(self):
        book = Book.objects.create(title='The Test1', isbn='34r49n3r8', description='Test description')
        review=Review.objects.create(user=self.user,book=book,stars_given=5,comment='Very delusional')
        response=self.client.get(reverse('api:review-detail',args=[review.id]))
        # test status code of response
        self.assertEqual(response.status_code,200)
        # test review info
        self.assertEqual(response.data['id'],review.id)
        self.assertEqual(response.data['stars_given'],5)
        self.assertEqual(response.data['comment'],'Very delusional')
        # test review user info
        self.assertEqual(response.data['user']['id'],review.user.id)
        self.assertEqual(response.data['user']['username'],'firdavs')
        self.assertEqual(response.data['user']['first_name'],'Firdavs')
        self.assertEqual(response.data['user']['last_name'],'Jalolov')
        # test review book info
        self.assertEqual(response.data['book']['id'],review.book.id)
        self.assertEqual(response.data['book']['title'],'The Test1')
        self.assertEqual(response.data['book']['description'],'Test description')
        self.assertEqual(response.data['book']['isbn'],'34r49n3r8')

    def test_review_list(self):
        book = Book.objects.create(title='The Test1', isbn='34r49n3r8', description='Test description')
        review1 = Review.objects.create(user=self.user, book=book, stars_given=5, comment='Very delusional')
        user_2 = CustomUser.objects.create_user(username='jemal',email='jemal@gmail.com',password='somepassword')
        review2 = Review.objects.create(user=user_2, book=book, stars_given=3, comment='Don\'t like that much')
        response=self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['count'],2)
        self.assertIn('next',response.data)
        self.assertIn('previous',response.data)
        self.assertEqual(len(response.data['results']),2)
        # test review details
        self.assertEqual(response.data['results'][1]['id'],review1.id)
        self.assertEqual(response.data['results'][1]['stars_given'],5)
        self.assertEqual(response.data['results'][1]['comment'],"Very delusional")
        self.assertEqual(response.data['results'][0]['id'],review2.id)
        self.assertEqual(response.data['results'][0]['stars_given'],3)
        self.assertEqual(response.data['results'][0]['comment'],"Don't like that much")

    def test_create_review(self):
        book = Book.objects.create(title='The Test1', isbn='34r49n3r8', description='Test description')
        response=self.client.post(reverse('api:review-list'),data={
            'stars_given':3,
            'comment':"An amazing book",
            'user_id':self.user.id,
            'book_id':book.id
        })
        review_obj=Review.objects.get(book=book,user=self.user)
        self.assertEqual(response.status_code,201)
        self.assertEqual(review_obj.stars_given,3)
        self.assertEqual(review_obj.comment,"An amazing book")
        self.assertEqual(review_obj.user.username,"firdavs")
        self.assertEqual(review_obj.book.title,"The Test1")

    def test_update_review(self):
        book = Book.objects.create(title='The Test1', isbn='34r49n3r8', description='Test description')
        review = Review.objects.create(user=self.user, book=book, stars_given=5, comment='Very too good')
        response=self.client.put(reverse('api:review-detail',kwargs={'review_id':review.id}),data={
            'stars_given':2,
            'comment':'Very too updated'
        })
        review.refresh_from_db()
        self.assertEqual(response.status_code,200)
        self.assertEqual(review.stars_given,2)
        self.assertEqual(review.comment,'Very too updated')

    def test_partial_update_review(self):
        book = Book.objects.create(title='The Hero', isbn='34r49n3r8', description='Test description')
        review = Review.objects.create(user=self.user, book=book, stars_given=5, comment='Very too good')
        response = self.client.patch(reverse('api:review-detail', kwargs={'review_id': review.id}), data={
            'comment': 'Very too partially updated'
        })
        review.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.comment, 'Very too partially updated')

    def test_delete_review(self):
        book = Book.objects.create(title='The Hero', isbn='34r49n3r8', description='Test description')
        review = Review.objects.create(user=self.user, book=book, stars_given=5, comment='Very too good')
        response=self.client.delete(reverse('api:review-detail',kwargs={'review_id':review.id}))
        self.assertEqual(response.status_code,204)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

