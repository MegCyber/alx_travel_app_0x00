# ALX Travel App 0x00 - Database Models and API Serializers

This is the enhanced version of the ALX Travel App with comprehensive database models, API serializers, and data seeding capabilities.

## 📋 Features

- **Database Models**: Listing, Booking, and Review models with proper relationships and constraints
- **API Serializers**: RESTful API serializers for data transformation
- **Data Seeding**: Management command to populate database with sample data
- **UUID Primary Keys**: Enhanced security with UUID-based primary keys
- **Data Validation**: Comprehensive validation rules and constraints
- **Swagger Documentation**: Auto-generated API documentation

## 🗃️ Database Models

### Listing Model
- **Primary Key**: UUID-based listing_id
- **Fields**: title, description, location, price_per_night, bedrooms, bathrooms, max_guests
- **Relationships**: ForeignKey to User (host), OneToMany with Bookings and Reviews
- **Features**: Average rating calculation, amenities management

### Booking Model
- **Primary Key**: UUID-based booking_id
- **Fields**: check_in_date, check_out_date, number_of_guests, total_price, status
- **Relationships**: ForeignKey to Listing and User
- **Validation**: Date constraints, guest count validation
- **Status Options**: pending, confirmed, canceled, completed

### Review Model
- **Primary Key**: UUID-based review_id
- **Fields**: rating (1-5 stars), comment
- **Relationships**: ForeignKey to Listing and User
- **Constraints**: One review per user per listing

## 🚀 API Endpoints

### Listings
- `GET /api/v1/listings/` - List all listings
- `POST /api/v1/listings/` - Create new listing
- `GET /api/v1/listings/{id}/` - Get listing details
- `PUT/PATCH /api/v1/listings/{id}/` - Update listing
- `DELETE /api/v1/listings/{id}/` - Delete listing

### Bookings
- `GET /api/v1/bookings/` - List user bookings
- `POST /api/v1/bookings/` - Create new booking
- `GET /api/v1/bookings/{id}/` - Get booking details
- `PUT/PATCH /api/v1/bookings/{id}/` - Update booking
- `DELETE /api/v1/bookings/{id}/` - Cancel booking

### Reviews
- `GET /api/v1/listings/{id}/reviews/` - List listing reviews
- `POST /api/v1/listings/{id}/reviews/` - Create review
- `PUT/PATCH /api/v1/reviews/{id}/` - Update review
- `DELETE /api/v1/reviews/{id}/` - Delete review

## 🛠️ Setup Instructions

### 1. Project Setup
```bash
# Navigate to project directory
cd ~/alx_travel_app_0x00

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Create and apply migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser (optional)
python3 manage.py createsuperuser
```

### 3. Seed Database
```bash
# Seed with default data
python3 manage.py seed

# Custom seeding options
python3 manage.py seed --listings 20 --users 10 --bookings 30 --reviews 50

# Clean existing data before seeding
python3 manage.py seed --clean --listings 15 --users 8
```

### 4. Run Development Server
```bash
python3 manage.py runserver
```

## 📊 Seeding Command Options

The `seed` management command supports the following options:

- `--listings N`: Number of listings to create (default: 20)
- `--users N`: Number of users to create (default: 10)
- `--bookings N`: Number of bookings to create (default: 30)
- `--reviews N`: Number of reviews to create (default: 50)
- `--clean`: Clean existing data before seeding

### Example Usage
```bash
# Seed with custom numbers
python3 manage.py seed --listings 25 --users 15 --bookings 40 --reviews 60

# Clean and seed with default numbers
python3 manage.py seed --clean

# Get help on available options
python3 manage.py seed --help
```

## 🔗 API Documentation

Once the server is running, access the API documentation:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **JSON Schema**: http://127.0.0.1:8000/swagger.json

## 📁 Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app/          # Main project directory
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── ...
├── listings/                # Listings app
│   ├── models.py            # Database models (Listing, Booking, Review)
│   ├── serializers.py       # API serializers
│   ├── views.py             # API views
│   ├── urls.py              # App URL configuration
│   ├── management/          # Management commands
│   │   └── commands/
│   │       └── seed.py      # Database seeding command
│   └── migrations/          # Database migrations
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── db.sqlite3              # SQLite database
└── README.md               # This file
```

## 🧪 Testing the API

### Using curl
```bash
# Get all listings
curl http://127.0.0.1:8000/api/v1/listings/

# Get health check
curl http://127.0.0.1:8000/api/v1/health/

# Get specific listing (replace with actual UUID)
curl http://127.0.0.1:8000/api/v1/listings/{listing-uuid}/
```

### Using Python requests
```python
import requests

# Get all listings
response = requests.get('http://127.0.0.1:8000/api/v1/listings/')
print(response.json())

# Get health check
response = requests.get('http://127.0.0.1:8000/api/v1/health/')
print(response.json())
```

## 🔐 Model Relationships

- **User ↔ Listing**: One-to-Many (User can host multiple listings)
- **User ↔ Booking**: One-to-Many (User can have multiple bookings)
- **User ↔ Review**: One-to-Many (User can write multiple reviews)
- **Listing ↔ Booking**: One-to-Many (Listing can have multiple bookings)
- **Listing ↔ Review**: One-to-Many (Listing can have multiple reviews)
- **User ↔ Listing (Review)**: Many-to-Many through Review (One review per user per listing)

## 📈 Data Validation

### Listing Validation
- Price per night must be positive
- Maximum guest count must be at least 1
- All required fields must be provided

### Booking Validation
- Check-out date must be after check-in date
- Number of guests cannot exceed listing capacity
- Total price must be positive
- At least one guest required

### Review Validation
- Rating must be between 1 and 5 stars
- One review per user per listing
- Comment is required

## 🔧 Database Constraints

- Check constraints for date validation
- Unique constraints for user-listing reviews
- Foreign key constraints for data integrity
- Index optimization for common queries

## 📝 Sample Data

The seeding command creates realistic sample data including:

- **Users**: Diverse user profiles with realistic names
- **Listings**: Various property types across major cities
- **Bookings**: Different booking statuses and date ranges
- **Reviews**: Realistic ratings and comments

## 🌟 Next Steps

This foundation supports building:
- Advanced search and filtering
- Payment processing integration
- Real-time availability checking
- Advanced analytics and reporting
- Mobile app integration
- Third-party service integrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is part of the ALX Software Engineering program.

---

**Happy Coding!** 🚀