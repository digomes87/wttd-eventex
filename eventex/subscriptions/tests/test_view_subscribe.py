from django.core import mail
from django.test import TestCase
from eventex.subscriptions.form import SubscriptionForm

""" Start you app always with test """


class SubscribeGet(TestCase):
    def setUp(self):
        """Defaul test resp return"""
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="email"', 1),
                ('type="submit', 1)
                )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html must contains csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Diego Go", cpf="01516712345", email="diego.gomes87@gmail.com", phone="41-995062619")
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valida POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class SubscriptionPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/')

    def test_post(self):
        """Invalid POst should be no redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_errors_form(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscriptionSuccessesMessage(TestCase):
    def test_message(self):
        data = dict(name="Diego Go", cpf="01516712345", email="diego.gomes87@gmail.com", phone="41-995062619")

        resp = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(resp, 'Inscrição realizada com sucesso')