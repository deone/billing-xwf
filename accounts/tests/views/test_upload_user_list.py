from django.core.urlresolvers import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.conf import settings

from ...models import GroupAccount
from ...forms import BulkUserUploadForm
from ...views import upload_user_list

from . import GroupAdminViewsTests 

import os

class UploadUserListTests(GroupAdminViewsTests):

    def test_upload_user_list_post(self):
        group = GroupAccount.objects.create(name='CUG', max_no_of_users=10)
        self.subscriber.group = group
        self.subscriber.save()

        with open(os.path.join(settings.BASE_DIR, 'accounts/tests/test_files/test.csv'), 'r') as _file:
            request = self.factory.post(reverse('accounts:upload_user_list'), {'user_list': _file})

        request.user = self.user

        self.session.process_request(request)
        request.session.save()

        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = upload_user_list(request)
        storage = get_messages(request)

        lst = []
        for message in storage:
            lst.append(message)

        self.assertEqual(response.status_code, 302)
        self.assertEqual('Users added successfully.', lst[0].__str__())
        self.assertEqual(response.get('location'), reverse('accounts:upload_user_list'))

    def test_upload_user_list_get(self):
        self.c.post(reverse('accounts:login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('accounts:upload_user_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('file_length' in response.context)
        self.assertEqual(response.context['file_length'], settings.MAX_FILE_LENGTH)
        self.assertTrue(isinstance(response.context['form'], BulkUserUploadForm))
        self.assertTemplateUsed(response, 'accounts/upload_user_list.html')
