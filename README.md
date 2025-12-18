# Warehouse Management System (WMS)

A comprehensive warehouse management system built with FastAPI, providing RESTful APIs for managing warehouse operations including inventory, orders, users, and authentication.

## 📁 Project Structure

```
iTechVision/
├── app/
│   ├── db/                    # Database configuration and models
│   │   ├── app.db            # SQLite database file
│   │   ├── base.py           # Database base configuration
│   │   └── session.py        # Database session management
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── order.py          # Order model
│   │   ├── product.py        # Product model
│   │   └── user.py           # User model
│   ├── routers/              # API route handlers
│   │   ├── auth_router.py    # Authentication endpoints
│   │   ├── order_router.py   # Order management endpoints
│   │   ├── product_router.py # Product management endpoints
│   │   └── user_router.py    # User management endpoints
│   ├── schemas/              # Pydantic schemas for request/response validation
│   │   ├── auth.py           # Authentication schemas
│   │   ├── order.py          # Order schemas
│   │   ├── product.py        # Product schemas
│   │   └── user.py           # User schemas
│   ├── services/             # Business logic layer
│   │   ├── auth.py           # Authentication service
│   │   ├── order.py          # Order service
│   │   ├── product.py        # Product service
│   │   └── user.py           # User service
│   ├── main.py               # Application entry point - FastAPI app initialization
│   └── utils.py              # Utility functions and helper methods
├── venv/                     # Virtual environment (gitignored)
├── .env                      # Environment variables (create from .env.example)
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

## 🚀 Setup Instructions

### 1. Create and Activate Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory using `.env.example` as a template:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration settings.

### 4. Run the Application

Navigate to the `iTechVision` directory and run:

```bash
python -m app.main
```

The application will start on `http://127.0.0.1:8000`

### 5. API Documentation

Once the application is running, access the interactive API documentation at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🗄️ Database Management

This project uses SQLite as the database.

### Viewing the Database

1. **Download SQLite Tools:**

   - Visit [sqlite.org](https://www.sqlite.org/download.html)
   - Download the SQLite tools zip file for your operating system

2. **Setup SQLite:**

   - Extract the zip file
   - Copy the contents to `C:\sqlite` (Windows) or your preferred location
   - Add the SQLite directory to your system's PATH environment variable

3. **Access the Database:**

```bash
   cd iTechVision/app/db
   sqlite3 ./app.db
```

4. **Useful SQLite Commands:**

```sql
   .tables              -- List all tables
   .schema table_name   -- Show table structure
   SELECT * FROM table_name;  -- Query data
   .quit                -- Exit SQLite
```

## 📦 Key Components

### `main.py`

- FastAPI application initialization
- Router registration
- CORS middleware configuration
- Application startup and shutdown events

### `utils.py`

- Helper functions and utilities
- Common operations used across the application
- Utility methods for data processing and validation

### Folder Responsibilities

- **`db/`** - Database connection, configuration, and session management
- **`models/`** - SQLAlchemy ORM models defining database schema
- **`routers/`** - API endpoint definitions and route handlers
- **`schemas/`** - Pydantic models for request/response validation and serialization
- **`services/`** - Business logic layer containing core application functionality

## 🛠️ Technologies Used

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **SQLite** - Lightweight relational database
- **Python 3.x** - Programming language
