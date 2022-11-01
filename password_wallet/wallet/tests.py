from django.test import TransactionTestCase
from .models import Password
from .views import PasswordListView
from unittest.mock import patch
from django.contrib import auth
from users.models import CustomUser
from django.urls import reverse
from users.tests import get_message
from .aes import AESCipher


class ListPasswordsCase(TransactionTestCase):
    reset_sequences = True

    def test_list_passwords_success(self):
        user = CustomUser.objects.create_user(login="some_login", password="some_password")
        pass1 = Password.objects.create(password_to_wallet="some_password1", login="some_login1", user=user)
        pass2 = Password.objects.create(password_to_wallet="some_password2", login="some_login1", user=user)
        self.client.login(login="some_login", password="some_password")

        response = self.client.get(reverse("wallet:wallet"))

        self.assertListEqual(list(response.context["object_list"]), [pass1, pass2])
        self.assertEqual(response.status_code, 200)

    def test_list_passwords_not_auth(self):
        response = self.client.get(reverse("wallet:wallet"), follow=True)

        self.assertRedirects(response, "/?next=/wallet/")


class CreatePasswordCase(TransactionTestCase):
    reset_sequences = True

    def test_create_password_success(self):
        user = CustomUser.objects.create_user(login="some_login", password="some_password")
        self.client.login(login="some_login", password="some_password")

        payload = {
            "password_to_wallet": "some_password",
            "user": user
        }

        response = self.client.post(reverse("wallet:add"), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("wallet:wallet"))
        self.assertEqual(get_message(response), "You successful created password!")

    def test_create_passwords_not_auth(self):
        response = self.client.get(reverse("wallet:add"), follow=True)

        self.assertRedirects(response, "/?next=/wallet/add/")


class DeletePasswordCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(login="some_login", password="some_password")
        self.pass1 = Password.objects.create(password_to_wallet="some_password1", login="some_login1", user=self.user)

    def test_delete_password_success(self):
        self.client.login(login="some_login", password="some_password")

        response = self.client.post(reverse("wallet:delete", args=(self.pass1.id, )), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("wallet:wallet"))
        self.assertEqual(get_message(response), "You successful deleted password!")

    def test_delete_password_not_auth(self):
        response = self.client.post(reverse("wallet:delete", args=(self.pass1.id,)), follow=True)

        self.assertRedirects(response, "/?next=/wallet/1/delete/")


class UpdatePasswordCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(login="some_login", password="some_password")
        self.pass1 = Password.objects.create(password_to_wallet="some_password1", login="some_login1", user=self.user)
        self.payload = {
            "password_to_wallet": "some_new_password",
            "user": self.user
        }

    def test_update_password_success(self):
        self.client.login(login="some_login", password="some_password")

        response = self.client.post(reverse("wallet:update", args=(self.pass1.id, )), self.payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("wallet:wallet"))
        self.assertEqual(get_message(response), "You successful updated password!")

    def test_update_password_not_auth(self):
        response = self.client.post(reverse("wallet:update", args=(self.pass1.id,)), self.payload, follow=True)

        self.assertRedirects(response, "/?next=/wallet/1/update/")


class IfCheckPasswordCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(login="some_login", password="some_password")
        self.pass1 = Password.objects.create(password_to_wallet="some_password1", login="some_login1", user=self.user)

    @patch.object(AESCipher, "decrypt", return_value="some_value")
    def test_get_password_if_checked_before(self, mock_decrypt):
        self.user.is_password_checked = True
        self.user.save()
        self.client.login(login="some_login", password="some_password")

        response = self.client.get(reverse("wallet:check", args=(self.pass1.id, )), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("wallet:show", args=(self.pass1.id, )))
        self.assertTrue(mock_decrypt.called)
        self.assertTemplateNotUsed(response, "wallet/master_password_check.html")
        self.assertTemplateUsed(response, "wallet/password_show.html")

    def test_not_get_password_if_not_checked_before(self):
        self.client.login(login="some_login", password="some_password")

        response = self.client.get(reverse("wallet:check", args=(self.pass1.id, )), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wallet/master_password_check.html")
        self.assertTemplateNotUsed(response, "wallet/password_show.html")

    @patch.object(AESCipher, "decrypt", return_value="some_value")
    def test_get_password_enter_master_password_success(self, mock_decrypt):
        self.client.login(login="some_login", password="some_password")

        payload = {
            "password": "some_password"
        }
        response = self.client.post(reverse("wallet:check", args=(self.pass1.id, )), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("wallet:show", args=(self.pass1.id, )))
        self.assertTrue(mock_decrypt.called)

    def test_not_get_password_enter_master_password_invalid(self):
        self.client.login(login="some_login", password="some_password")

        payload = {
            "password": "some_password1111"
        }

        response = self.client.post(reverse("wallet:check", args=(self.pass1.id, )), payload, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_message(response), "Password is incorrect!")

    def test_not_get_password_check_not_auth(self):
        response = self.client.get(reverse("wallet:check", args=(self.pass1.id,)), follow=True)

        self.assertRedirects(response, "/?next=/wallet/1/check/")


class DecryptingPasswordCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(login="some_login", password="some_password")
        cipher = AESCipher()

        enc_pass = cipher.encrypt("some_password1")
        self.pass1 = Password.objects.create(password_to_wallet=enc_pass.decode(), login="some_login1", user=self.user)

    def test_get_encrypted_password_decrypted_success(self):
        self.user.is_password_checked = True
        self.user.save()
        self.client.login(login="some_login", password="some_password")

        response = self.client.get(reverse("wallet:show", args=(self.pass1.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("password"), "some_password1")

    def test_not_get_password_show_not_auth(self):
        response = self.client.get(reverse("wallet:show", args=(self.pass1.id,)), follow=True)

        self.assertRedirects(response, "/?next=/wallet/")