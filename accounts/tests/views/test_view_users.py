from django.core.urlresolvers import reverse

from . import ViewsTests

from ...views import view_users

class ViewUsersTests(ViewsTests):

    def test_view_users_get(self):
        request = self.factory.post(reverse('accounts:users'))
        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        response = view_users(request, page=2, paginate_by=5)
        self.assertEqual(response.status_code, 200)
