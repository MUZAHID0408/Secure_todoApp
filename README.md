# Todo API - FastAPI Backend Application

A professional, secure, and scalable Todo management system built with FastAPI. Features complete user authentication, role-based access control, and a full CRUD API for todo management.

## 🚀 Features

- **🔐 Secure Authentication**
  - JWT token-based authentication
  - Bcrypt password hashing
  - Role-based authorization (Admin/User)
- **📝 Todo Management**
  - Complete CRUD operations
  - User-specific todo isolation
  - Priority-based organization
- **👥 User Management**
  - User registration and profile management
  - Password change functionality
  - Admin user management
- **🛡️ Security**
  - Input validation with Pydantic
  - SQL injection protection
  - Secure password policies
- **📚 API Documentation**
  - Auto-generated Swagger UI
  - Interactive ReDoc documentation

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JOSE)
- **Password Hashing**: Bcrypt (Passlib)
- **Validation**: Pydantic v2
- **API Documentation**: Auto-generated OpenAPI

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   https://github.com/MUZAHID0408/Secure_todoApp.git
   cd Secure_todoApp
   ```
   
2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate	
   ```   
      
      
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```  
      
      
4. **Initialize the database**

   ```bash
   python main.py
   ```
   
   
## 🚀 Running the Application
```bash
 uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The application will be available at: http://localhost:8000    



## 📚 API Documentation
   **Once running, access the interactive API documentation:**

	 - Swagger UI: http://localhost:8000/docs

	 - ReDoc: http://localhost:8000/redoc


##🔐 API Endpoints

### Authentication (/auth)
**POST** `/auth/` - Register new user  
**POST** `/auth/token` - Login and get JWT token  

### Todos (/)
**GET** `/` - Get all todos for authenticated user  
**GET** `/todo/{todo_id}` - Get specific todo  
**POST** `/todo/insert` - Create new todo  
**PUT** `/todo/update/{todo_id}` - Update todo  
**DELETE** `/todo/delete/{todo_id}` - Delete todo  

### User Management (/user)
**GET** `/user/active_user` - Get current user profile  
**POST** `/user/change_password` - Change user password  

### Admin (/admin) - Admin only
**GET** `/admin/todo` - Get all todos (admin access)  
**DELETE** `/admin/todo/delete/{todo_id}` - Delete any todo


## 🗄️ Database Models

### Users
- `id` (Primary Key)  
- `email` (Unique)  
- `username` (Unique)  
- `firstname`, `lastname`  
- `hashed_password`  
- `is_active` (Boolean)  
- `role` (String)  

### Todos
- `id` (Primary Key)  
- `title`, `description`  
- `priority` (Integer)  
- `complete` (Boolean)  
- `user` (Foreign Key to Users)  

### 👥 User Roles
- **User:** Can manage own todos and profile  
- **Admin:** Full access to all users and todos  

### 🔒 Security Features
- Password hashing with bcrypt  
- JWT token authentication  
- Role-based authorization middleware  
- Input validation with Pydantic models  
- SQL injection protection via SQLAlchemy  
- CORS middleware enabled       
     
     

## 📂 Project Structure

```text
todo-fastapi-backend/
├── main.py              # Application entry point
├── database.py          # Database configuration
├── model.py             # SQLAlchemy models
├── requirements.txt     # Project dependencies
├── routers/             # API route modules
│   ├── auth.py          # Authentication routes
│   ├── todos.py         # Todo management
│   ├── admin.py         # Admin routes
│   └── users.py         # User management
└── todos_app.db         # SQLite database (auto-generated)  
```

## 🧪 Testing the API

### 1. Create a User

```bash
curl -X POST "http://localhost:8000/auth/" \
-H "Content-Type: application/json" \
-d '{
  "email": "user@example.com",
  "username": "testuser",
  "firstname": "John",
  "lastname": "Doe",
  "password": "securepassword",
  "is_active": true,
  "role": "user"
}'
```

### 2. Get Access Token

```bash
curl -X POST "http://localhost:8000/auth/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=testuser&password=securepassword"
```

###3. Use the Token for Authenticated Requests

```bash
curl -X GET "http://localhost:8000/" \
-H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```


## 📦 Dependencies

Create a `requirements.txt` file with:

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
bcrypt==4.1.2
pydantic==2.5.0
alembic==1.12.1
```

## 🚨 Error Handling

The API provides comprehensive error handling for:

- Authentication failures (401)
- Authorization failures (403)
- Resource not found (404)
- Validation errors (422)
- Internal server errors (500)


## 🆘 Support

If you encounter any issues:

1. Check the auto-generated API documentation at `/docs`
2. Review the existing issues on GitHub
3. Create a new issue with detailed information

## 🙏 Acknowledgments

- **FastAPI** team for the excellent framework  
- **SQLAlchemy** for robust ORM capabilities  
- **Pydantic** for data validation and serialization  

---

**Note:** This is a backend API service. For a complete application, you'll need to build a frontend client that consumes these RESTful endpoints.

```txt
And here's the `requirements.txt` file content:

fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
bcrypt==4.1.2
pydantic==2.5.0
alembic==1.12.1
```

   
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
