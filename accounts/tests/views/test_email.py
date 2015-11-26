from django.core.urlresolvers import reverse

from ...views import resend_mail
from ...helpers import make_context
from ...models import Subscriber

from . import ViewsTests

class EmailTests(ViewsTests):

    def test_verify_email(self):
        self.subscriber.email_verified = False
        self.subscriber.date_verified = None
        self.subscriber.save()

        request = self.factory.get(reverse('index'))
        context = make_context(self.user)

        response = self.c.get(reverse('accounts:verify_email',
          kwargs={'uidb64':context['uid'], 'token': context['token']}))

        subscriber = Subscriber.objects.get(pk=self.subscriber.pk)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:dashboard'),
            status_code=302, target_status_code=302)
        self.assertEqual(subscriber.email_verified, True)
        self.assertNotEqual(subscriber.date_verified, None)

    def test_verify_email_404(self):
        response = self.c.get(reverse('accounts:verify_email',
          kwargs={'uidb64':'Ng', 'token': '44l-013ea9fff05d175d1ccb'}))
        self.assertEqual(response.status_code, 404)

    def test_resend_mail(self):
        request = self.factory.get(reverse('index'))
        request.user = self.user
        response = resend_mail(request)
        self.assertEqual(response.status_code, 302)
