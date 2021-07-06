from django.test import TestCase
from users.views import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group


class TestUsers(TestCase):
    def setUp(self):
        estabelecimentoGroup = Group.objects.create(name="noGroupEstabelecimento")
        freelancerGroup = Group.objects.create(name="noGroupFreelancer")

        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com',
            'password1'
        )
        self.token = Token.objects.create(user=self.writer)

        self.writer2 = User.objects.create_user(
            'teste@trampoja.com',
            'teste@trampoja.com',
            '123456'
        )


class TestUsersCreateView(TestUsers):
    def test_create_users_post_sucess(self):
        data = {
            'username': 'joao@gmail.com',
            'password': '123456',
            'email': 'joao@gmail.com',
            'first_name': 'Joao',
            'last_name': 'Antunes'
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 201)

    def test_create_users_post_sucess_com_br(self):
        data = {
            'username': 'joao@gmail.com.br',
            'password': '123456',
            'email': 'joao@gmail.com.br',
            'first_name': 'Joao',
            'last_name': 'Antunes'
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 201)

    def test_create_users_post_invalid_name(self):
        data = {
            'username': 'joao@gmail.com.br',
            'password': '123456',
            'email': 'joao@gmail.com.br',
            'first_name': 'Joa1',
            'last_name': 'Antunes'
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 400)

    def test_create_users_post_error_password(self):
        data = {
            'username': 'test@test.com',
            'password': '12345',
            'email': 'test@test.com',
            'first_name': 'Joao',
            'last_name': 'Antunes'
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 400)

    def test_create_users_post_error(self):
        data = {
            'username': '',
            'password': '123456',
            'email': '',
            'first_name': '',
            'last_name': ''
        }
        response = self.client.post("/auth/register", data)
        self.assertEqual(response.status_code, 400)


class TestUserSetGroupView(TestUsers):
    def test_set_group_freelancer_sucess(self):
        data = {
            'group': 'noGroupFreelancer'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/auth/set-group", data)
        self.assertEqual(response.status_code, 200)

    def test_set_group_estabelecimento_sucess(self):
        data = {
            'group': 'noGroupEstabelecimento'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/auth/set-group", data)
        self.assertEqual(response.status_code, 200)

    
    def test_set_group_error(self):
        data = {
            'group': 'invalid'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/auth/set-group", data)
        self.assertEqual(response.data, None)

    def test_set_group_auth(self):
        data = {
            'group': 'noGroupEstabelecimento'
        }
        response = self.client.post("/auth/set-group", data)
        self.assertEqual(response.status_code, 302)


class TestUsersProfileView(TestUsers):
    def test_profile_user_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.get("/auth/profile")
        self.assertEqual(response.status_code, 401)

    def test_profile_user_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/auth/profile")
        self.assertEqual(response.status_code, 200)


class TestUsersDetailView(TestUsers):
    def test_detail_user_error(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/auth/detail/0")
        self.assertEqual(response.status_code, 404)

    def test_detail_user_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get("/auth/detail/1")
        self.assertEqual(response.status_code, 200)


class TestChangeEmailView(TestUsers):
    def test_set_email_post_error(self):
        data = {
            'email': '',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put("/auth/set-email", data)
        self.assertEqual(response.status_code, 400)

    def test_set_email_post_sucess(self):
        data = {
            'email': 'test3@test.com',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/auth/set-email", data)
        self.assertEqual(response.status_code, 200)


class TestChangePasswordView(TestUsers):
    def test_set_password_sucess(self):
        data = {
            'password': '654321'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/auth/set-password", data)
        self.assertEqual(response.status_code, 200)

    def test_set_password_invalid(self):
        data = {
            'password': '65432'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post("/auth/set-password", data)
        self.assertEqual(response.status_code, 400)

    def test_set_password_error(self):
        data = {
            'password': '654321'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response = self.client.post("/auth/set-password", data)
        self.assertEqual(response.status_code, 401)


class TestRecoveryPasswordView(TestUsers):
    def test_recovery_password_sucess(self):
        data = {
            'email': 'teste@trampoja.com'
        }
        response = self.client.post("/auth/recovery-pswd", data)
        self.assertEqual(response.status_code, 200)

    def test_recovery_password_error_email_not_exist(self):
        data = {
            'email': 'test@gmail.com'
        }
        response = self.client.post("/auth/recovery-pswd", data)
        self.assertEqual(response.status_code, 404)


class TestLogin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.writer = User.objects.create_user(
            'test_user',
            'test@example.com',
            'password1'
        )

    def test_login_sucess(self):

        data = {
            'username': 'test_user',
            'password': 'password1'
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, 200)

    def test_login_error(self):

        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, 400)

    def test_login_error_password(self):

        data = {
            'username': self.writer.username,
            'password': ''
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, 400)

    def test_login_error_username(self):

        data = {
            'username': '',
            'password': self.writer.password
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, 400)
