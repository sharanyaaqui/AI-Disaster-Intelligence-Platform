# AI Disaster Intelligence Platform
## Backend API Documentation

---

# Authentication APIs

## Register User

POST `/register`

Request:
```json
{
    "full_name": "Janvi Singh",
    "email": "janvi@gmail.com",
    "password": "123456",
    "language": "en"
}