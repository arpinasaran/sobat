from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from forum.models import Question, Answer
from product.models import DrugEntry

User = get_user_model()

class ForumViewTests(TestCase):
    def setUp(self):
        # Set up test data and authenticated user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        
        # Create a sample product
        self.drug = DrugEntry.objects.create(
            name="Test Drug",
            description="A test drug description",
            category="Test Category",
            drug_type="Test Type",
            drug_form="Test Form",
            price=10.0,
            availability=True
        )

        # Create a sample question
        self.question = Question.objects.create(
            question_title="Test Question",
            question="This is a test question",
            user=self.user,
            drug_asked=self.drug
        )

    def test_show_forum(self):
        response = self.client.get(reverse('show_forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum.html')

    def test_add_question_ajax(self):
        url = reverse('add_question_ajax', args=[self.drug.id])
        data = {
            'question_title': 'New Test Question',
            'question': 'This is a new test question.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Question.objects.filter(question_title='New Test Question').exists())

    def test_show_answers(self):
        response = self.client.get(reverse('show_answers', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'answers.html')

    def test_like_question(self):
        url = reverse('like_question', args=[self.question.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.question.likes.filter(id=self.user.id).exists())

        # Test unlike
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.question.likes.filter(id=self.user.id).exists())

    def test_delete_question(self):
        url = reverse('delete_question', args=[self.question.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Question.objects.filter(id=self.question.id).exists())

    def test_add_answer(self):
        url = reverse('answer_question', args=[self.question.id, self.drug.id])
        data = {
            'answer': 'This is a test answer.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Answer.objects.filter(answer='This is a test answer.').exists())

    def test_like_answer(self):
        answer = Answer.objects.create(answer='Test Answer', user=self.user, question=self.question)
        url = reverse('like_answer', args=[answer.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(answer.likes.filter(id=self.user.id).exists())

        # Test unlike
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(answer.likes.filter(id=self.user.id).exists())

    def test_delete_answer(self):
        answer = Answer.objects.create(answer='Answer to delete', user=self.user, question=self.question)
        url = reverse('delete_answer', args=[answer.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Answer.objects.filter(id=answer.id).exists())

    def test_show_json_question(self):
        response = self.client.get(reverse('show_json_question'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_show_json_answer(self):
        url = reverse('show_json_answer', args=[self.question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())
