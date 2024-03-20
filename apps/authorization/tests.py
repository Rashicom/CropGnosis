from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from apps.authorization.views import customer_views, mentor_view
from apps.authorization.models import Accounts

"""-------------------------Customer Tests--------------------------"""

class CustomerAccountRequestTest(APITestCase):

    # user registration
    def test_authentication_requests(self):
        data = {
            "name":"test_name",
            "contact_number":"9846142484",
            "email":"testemail@gmail.com",
            "password":"123"
        }
        factory = APIRequestFactory()
        request = factory.post("/api/customer/registration/", data, format='json')
        view = customer_views.UserRegistration.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200, "User registration Failed")

        # duplicate registration
        dup_request = factory.post("/api/customer/registration/", data, format='json')
        view = customer_views.UserRegistration.as_view()
        dup_response = view(dup_request)
        self.assertEqual(dup_response.status_code, 400, "Duplicate user registraion Failde")

        # login user
        login_request = factory.post(
            "/api/customer/login",
            {"email":"testemail@gmail.com","password":"123"},
            format='json'
        )
        view = customer_views.UserLogin.as_view()
        login_response = view(login_request)
        self.assertEqual(login_response.status_code, 200, "Login Failed")

        # login user
        login_request = factory.post(
            "/api/customer/login",
            {"email":"wrongmail@gmail.com","password":"123"},
            format='json'
        )
        login_response = view(login_request)
        self.assertEqual(login_response.status_code, 401, "Wrong Email Test Fialed")


    def test_usertype_login_restriction(self):
        """
        login restricted for users they are not farmers
        """
        farmer_user = Accounts.objects.create_user(email="testuser@gmail.com", password="123", user_type="MENTOR")
        factory = APIRequestFactory()
        view = customer_views.UserLogin.as_view()
        login_request = factory.post(
            "/api/customer/login",
            {"email":"testuser@gmail.com","password":"123"},
            format='json'
        )
        response = view(login_request)
        self.assertEqual(response.status_code,401, "User type restriction Failed")

    
    # TODO: account address testig