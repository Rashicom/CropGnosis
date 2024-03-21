from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate
from apps.authorization.views import customer_views, mentor_view
from apps.authorization.models import Accounts
import json

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

    
    def test_account_address(self):

        # test post
        farmer_user = Accounts.objects.create_user(email="testuser@gmail.com", password="123", user_type="FARMER")
        address_data = {
            "place":"test_place",
            "city":"test_city",
            "state":"test_state",
            "zip_code":"111111",
            "about":"test about",
            "designation":"test designation",
            "mentor_fee":1000
        }
        factory = APIRequestFactory()
        view = customer_views.AccountAddress.as_view()
        request = factory.post(
            "/api/customer/address",
            address_data,
            format='json'
        )
        force_authenticate(request,farmer_user)
        response = view(request)
        self.assertEqual(response.status_code, 200, "Address creation Failed")

        # test patch
        address_update = {"city":"edited city"}
        request = factory.patch(
            "/api/customer/address",
            address_update,
            format='json'
        )
        force_authenticate(request,farmer_user)
        updation_response = view(request)
        self.assertEqual(updation_response.status_code,200, "Address Updation Failed")
        
        # test data updated or not
        self.assertContains(updation_response, "edited city", status_code=200)

        # gest get
        request = factory.get(
            "/api/customer/address",
            address_update,
            format='json'
        )
        force_authenticate(request,farmer_user)
        response = view(request)
        self.assertContains(response,"edited city", status_code=200)

