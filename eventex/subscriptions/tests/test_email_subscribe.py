from unittest import TestCase
from django.core import mail


class SubscribePostValid(TestCase):
    def setUp(self):
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'diego.gomes87@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Diego Go',
            '01516712345',
            'diego.gomes87@gmail.com',
            '41-995062619'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

