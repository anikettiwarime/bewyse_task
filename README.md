# README.md

## Django API

This Django API provides a simple authentication and profile management system.

## Installation

To install the API, you will need to have Python 3.9 or higher and Django 3.2 or higher installed on your system. You can install the dependencies using pip:

```python
pip install -r requirements.txt
```

You will also need to create a local MongoDB database and a Firebase project. Once you have created the database and project, you will need to set the following environment variables:

```.env
# True for development, False for production
DEBUG=True

# MONGO DATABASE CREDENTIALS
MONGO_HOST=mongodb://localhost:27017
MONGO_DATABASE=django
```

## API Endpoints

The API provides the following endpoints:

### Account Endpoints

* `/accounts/register/` (POST): Registers a new user.
* `/accounts/login/` (POST): Logs in a user and returns a custom token.
* `/accounts/profile/view/` (GET): Retrieves a user's profile information.
* `/accounts/profile/edit/` (POST): Updates a user's profile information.

### Authentication

All API endpoints, except for `/accounts/register/` and `/accounts/login/`, require authentication. To authenticate requests, you must send the `access` token header with the user's custom token.

## Example Usage

To register a new user, send a POST request to the `/accounts/register/` endpoint with the following JSON data in the request body:

```json
{
  "username": "my_username",
  "email": "my_email@example.com",
  "password": "my_password"
}
```

If the registration is successful, the response will contain a `custom_token` field. This token should be used to authenticate all subsequent requests to the API.

To log in a user, send a POST request to the `/accounts/login/` endpoint with the following JSON data in the request body:

```json
{
  "username": "my_username",
  "password": "my_password"
}
```

If the login is successful, the response will contain a `custom_token` field. This token should be used to authenticate all subsequent requests to the API.

To retrieve a user's profile information, send a GET request to the `/accounts/profile/view/` endpoint with the `custom_token` header set to the user's custom token.

To update a user's profile information, send a POST request to the `/accounts/profile/edit/` endpoint with the `custom_token` header set to the user's custom token and the following JSON data in the request body:

```json
{
  "first_name": "My First Name",
  "last_name": "My Last Name",
  "username": "my_new_username"
}
```

## Troubleshooting

If you are having trouble getting the API to work, please consult the Django documentation or the Firebase documentation.

## Additional Notes

* The API is designed to be used with a front-end application.
* The API can be easily extended to add new features, such as support for additional authentication methods or social login.
* The API is secure and uses best practices to protect user data.
