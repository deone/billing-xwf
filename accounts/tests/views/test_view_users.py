from django.core.urlresolvers import reverse

from . import GroupAdminViewsTests

from ...views import view_users

class ViewUsersTests(GroupAdminViewsTests):

    def test_view_users_get(self):
        request = self.factory.post(reverse('accounts:users'))
        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        response = view_users(request, page=2)
        self.assertEqual(response.status_code, 200)
