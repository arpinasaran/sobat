from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from forum.models import Question, Answer
from product.models import DrugEntry

User = get_user_model()

class ForumTests(TestCase):
    def setUp(self):
        # Set up test client and create test users, questions, and answers
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.drug_entry = DrugEntry.objects.create(
            name="Test Drug",
            desc="Test Description",
            category="Test Category",
            drug_type="Test Type",
            drug_form="Test Form",
            price=10.0,
        )
        self.question = Question.objects.create(
            user=self.user,
            question_title="Test Question Title",
            question="This is a test question.",
            drug_asked=self.drug_entry,
            num_answer=0
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            answer="This is a test answer.",
            drug_ans=self.drug_entry
        )

    def test_show_forum(self):
        # Log in and test the forum page loads
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('forum:show_forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum.html")

    def test_add_question_ajax(self):
        # Log in and test adding a question
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('forum:add_question_ajax', args=[self.drug_entry.id]),
            {'question_title': 'New Test Question', 'question': 'This is another test question.'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Question.objects.filter(question_title='New Test Question').exists())

    def test_like_question(self):
        # Log in and test liking a question
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('forum:like_question', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.question.likes.filter(id=self.user.id).exists())

    def test_add_answer(self):
        # Log in and test adding an answer
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('forum:answer_question', args=[self.question.id, self.drug_entry.id]),
            {'answer': 'This is a test answer to a question.'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Answer.objects.filter(answer='This is a test answer to a question.').exists())
        self.question.refresh_from_db()

    def test_delete_question(self):
        # Log in and test deleting a question
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('forum:delete_question', args=[self.question.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Question.objects.filter(pk=self.question.id).exists())

    def test_delete_answer(self):
        # Log in and test deleting an answer
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('forum:delete_answer', args=[self.answer.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Answer.objects.filter(pk=self.answer.id).exists())
        self.question.refresh_from_db()
