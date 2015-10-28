from django.core.urlresolvers import reverse

from ..forms import LoginForm
from . import ViewsTests

class CaptiveTests(ViewsTests):
    
    def test_captive(self):
        get_params = "?login_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogin%3Fmauth%3DMMzZUJGqtrsmvkKw6ktCkcNsuBgluav4m2vgE4p-nFliz6lOzP99ntPzZAjvJ_Yit73ZfWwRDIzoEAwzZSuErRpQwdfD0vVA3XjsLLlK8UNiucySNAij7FEqEAF9osnXpWioNcUpyn7BYW8pP5C-wdZAQpLAWS-lv4UTivlfTUn92n4RxMaWG52Q%26continue_url%3Dhttps%253A%252F%252Fn110.network-auth.com%252Fsplash%252Fconnected%253Fhide_terms%253Dtrue&continue_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Fconnected%3Fhide_terms%3Dtrue&ap_mac=00%3A18%3A0a%3Af2%3Ade%3A20&ap_name=Djungle+HQ+02&ap_tags=office-accra+recently-added&client_mac=4c%3A8d%3A79%3Ad7%3A6b%3A28&client_ip=192.168.2.65"
        response = self.c.get(''.join([reverse('captive'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')
        self.assertTrue(isinstance(response.context['form'], LoginForm))
        self.assertTrue('login_url' in response.context)
        self.assertTrue('success_url' in response.context)

    def test_captive_with_error_message(self):
        get_params = "?login_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogin%3Fmauth%3DMMzZUJGqtrsmvkKw6ktCkcNsuBgluav4m2vgE4p-nFliz6lOzP99ntPzZAjvJ_Yit73ZfWwRDIzoEAwzZSuErRpQwdfD0vVA3XjsLLlK8UNiucySNAij7FEqEAF9osnXpWioNcUpyn7BYW8pP5C-wdZAQpLAWS-lv4UTivlfTUn92n4RxMaWG52Q%26continue_url%3Dhttps%253A%252F%252Fn110.network-auth.com%252Fsplash%252Fconnected%253Fhide_terms%253Dtrue&error_message=Access+denied+for+herbertellisspectradjungle%40spectrawireless.com&continue_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Fconnected%3Fhide_terms%3Dtrue&ap_mac=00%3A18%3A0a%3Af2%3Ade%3A20&ap_name=Djungle+HQ+02&ap_tags=office-accra+recently-added&client_mac=4c%3A8d%3A79%3Ad7%3A6b%3A28&client_ip=192.168.2.65"
        response = self.c.get(''.join([reverse('captive'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('error_message' in response.context)

    def test_captive_without_get_params(self):
        response = self.c.get(reverse('captive'))
        self.assertEqual(response.status_code, 404)

    def test_success(self):
        get_params = "?logout_url=https%3A%2F%2Fn110.network-auth.com%2Fsplash%2Flogout%3Fkey%3DMM7n9oxmBMVzgXgqkvAbLsLTh2cP7lcZdnhrqPRdHlIqzFHCNSRkxoiKzMGmTDQw7dGd092BdPfUs"
        response = self.c.get(''.join([reverse('success'), get_params]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('logout_url' in response.context)

    def test_success_without_get_params(self):
        response = self.c.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
