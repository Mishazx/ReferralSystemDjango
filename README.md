# Referral System Django Project

This project is a Django-based referral system that provides an API for user authentication, verification, and profile management.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mishazx/ReferralSystemDjango
   cd RefferalSystemDjango
   ```

2. **Environment Variables:**
   - Copy `.template.env` to `.env` and adjust the values as needed.

3. **Build and Run the Docker Containers:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - The application will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- **POST /auth/**
  - Description: Authenticate user by phone number.
  - Request Body:
    ```json
    {
      "phone_number": "User phone number"
    }
    ```
  - Response:
    ```json
    {
      "message": "Code sent",
      "is_new_user": true,
      "code": "1234"
    }
    ```

### Verification

- **POST /verify/**
  - Description: Verify user by code.
  - Request Body:
    ```json
    {
      "phone_number": "User phone number",
      "code": "Verification code"
    }
    ```
  - Response:
    ```json
    {
      "message": "Verification successful"
    }
    ```

### User Profile

- **GET /profile/**
  - Description: Get user profile by phone number.
  - Query Parameter:
    - `phone_number`: Phone number of the user
  - Response:
    ```json
    {
      "phone_number": "User phone number",
      "other_fields": "..."
    }
    ```

### Activate Invite

- **POST /profile/invite/**
  - Description: Activate invite code for user.
  - Request Body:
    ```json
    {
      "phone_number": "User phone number",
      "invite_code": "Invite code to activate"
    }
    ```
  - Response:
    ```json
    {
      "message": "Invite code activated"
    }
    ```

## Running Tests

To run tests for the application, use the following command:
```bash
docker-compose exec web python manage.py test
```

## License

This project is licensed under the MIT License.