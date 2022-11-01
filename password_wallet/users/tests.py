from django.test import TransactionTestCase
from django.urls import reverse
from .models import CustomUser


def get_message(response):
    return [m.message for m in response.context.get('messages')][0]


class CreateCustomUserCase(TransactionTestCase):
    reset_sequences = True

    def test_create_user_success(self):
        payload = {"login": "some_login",
                   "password1": "some_password",
                   "password2": "some_password"}
        response = self.client.post(reverse("users:register"), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_message(response), "You successful registered user!")
        self.assertRedirects(response, reverse("users:login"))

    def test_create_user_invalid(self):
        payload = {"login": "some_login",
                   "password1": "some_password111",
                   "password2": "some_password"}
        response = self.client.post(reverse("users:register"), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        try:
            message = get_message(response)
        except IndexError:
            print("test_create_user_error - No message available")


class UpdateCustomUserCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        CustomUser.objects.create_user(login="some_login", password="some_password")

    def test_update_user_success(self):
        self.client.login(login="some_login", password="some_password")

        payload = {"old_password": "some_password",
                   "new_password1": "some_new_password",
                   "new_password2": "some_new_password"}
        response = self.client.post(reverse("users:password-change"), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_message(response), "Your password was successfully updated!")

    def test_update_user_invalid(self):
        self.client.login(login="some_login", password="some_password")

        payload = {"old_password": "some_password",
                   "new_password1": "some_new_password111111",
                   "new_password2": "some_new_password"}
        response = self.client.post(reverse("users:password-change"), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_message(response), "Please correct the error below.")

    def test_update_user_not_auth(self):
        response = self.client.get(reverse("users:password-change"), follow=True)

        self.assertRedirects(response, "/?next=/update-password/")


class DeleteCustomUserCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(login="some_login", password="some_password")

    def test_delete_user_success(self):
        self.client.login(login="some_login", password="some_password")
        response = self.client.post(reverse("users:delete", args=(self.user.id,)), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_message(response), "You successful deleted account!")
        self.assertRedirects(response, reverse("users:login"))

    def test_delete_user_not_auth(self):
        response = self.client.post(reverse("users:delete", args=(self.user.id,)), follow=True)

        self.assertRedirects(response, "/?next=/user/1/delete/")
