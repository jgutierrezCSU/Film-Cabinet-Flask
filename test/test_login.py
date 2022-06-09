import json
import requests
from website import create_app
""" Nomial Functional test """

# def test_login():
#     """
    
#     """
#     flask_app=create_app()
#     with flask_app.test_client() as test_client:
#         #GET
#         response=test_client.get('login')
#         #not logged in so redirect is expected
#         assert response.status_code == 308
#         #POST
#         response=test_client.post('login')
#         assert response.status_code == 308
#         send_data = {
#                 "emailLogin": "test@mail.com", 
#                 "password": "test1234"
#             }
#         response = test_client.post('http://127.0.0.1:5000/login',data=send_data)
#         print("r",response)    