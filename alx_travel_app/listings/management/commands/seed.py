"""
Management command to seed the database with sample data.
"""
import random
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    """
    Django management command to populate the database with sample listings,
    bookings, and reviews for development and testing purposes.
    """
    help = 'Seed the database with sample listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=50,
            help='Number of reviews to create (default: 50)'
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean existing data before seeding'
        )

    def handle(self, *args, **options):
        """Main command handler."""
        if options['clean']:
            self.stdout.write('Cleaning existing data...')
            self.clean_data()

        self.stdout.write('Starting database seeding...')
        
        # Create users
        users = self.create_users(options['users'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(users)} users')
        )
        
        # Create listings
        listings = self.create_listings(users, options['listings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(listings)} listings')
        )
        
        # Create bookings
        bookings = self.create_bookings(users, listings, options['bookings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(bookings)} bookings')
        )
        
        # Create reviews
        reviews = self.create_reviews(users, listings, options['reviews'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(reviews)} reviews')
        )
        
        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )

    def clean_data(self):
        """Clean existing data from the database."""
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        # Don't delete all users, just the ones we created
        User.objects.filter(username__startswith='user_').delete()

    def create_users(self, count):
        """Create sample users."""
        users = []
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@alxtravelapp.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            users.append(admin)
        
        # Sample user data
        first_names = [
            'John', 'Jane', 'Mike', 'Sarah', 'David', 'Emma', 'Chris', 'Lisa',
            'Tom', 'Anna', 'James', 'Maria', 'Robert', 'Jennifer', 'William'
        ]
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez'
        ]
        
        for i in range(count):
            username = f'user_{i+1:03d}'
            
            if not User.objects.filter(username=username).exists():
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    first_name=first_name,
                    last_name=last_name
                )
                users.append(user)
        
        return users

    def create_listings(self, users, count):
        """Create sample listings."""
        listings = []
        
        # Sample listing data
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
            'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Boston'
        ]
        
        property_types = [
            'Cozy Apartment', 'Luxury Villa', 'Beach House', 'Mountain Cabin',
            'City Loft', 'Country Cottage', 'Modern Condo', 'Historic Home',
            'Penthouse Suite', 'Charming Studio', 'Family House', 'Resort Room'
        ]
        
        amenities_list = [
            ['WiFi', 'Kitchen', 'Parking'],
            ['WiFi', 'Pool', 'Gym', 'Kitchen'],
            ['WiFi', 'Beach Access', 'Kitchen', 'Parking'],
            ['WiFi', 'Mountain View', 'Fireplace', 'Kitchen'],
            ['WiFi', 'City View', 'Gym', 'Rooftop'],
            ['WiFi', 'Garden', 'Kitchen', 'Parking'],
            ['WiFi', 'Kitchen', 'Balcony', 'Gym'],
            ['WiFi', 'Historic Features', 'Kitchen', 'Parking'],
            ['WiFi', 'City View', 'Luxury Amenities', 'Concierge'],
            ['WiFi', 'Kitchen', 'Parking'],
            ['WiFi', 'Kitchen', 'Backyard', 'Parking'],
            ['WiFi', 'Pool', 'Spa', 'Restaurant']
        ]
        
        for i in range(count):
            property_type = random.choice(property_types)
            city = random.choice(cities)
            amenities = random.choice(amenities_list)
            
            listing = Listing.objects.create(
                title=f'{property_type} in {city}',
                description=f'Beautiful {property_type.lower()} located in the heart of {city}. Perfect for travelers looking for comfort and convenience.',
                location=city,
                price_per_night=Decimal(str(random.randint(50, 500))),
                number_of_bedrooms=random.randint(1, 4),
                number_of_bathrooms=random.randint(1, 3),
                max_guest_count=random.randint(1, 8),
                host=random.choice(users),
                is_available=random.choice([True, True, True, False]),  # 75% available
                amenities=', '.join(amenities)
            )
            listings.append(listing)
        
        return listings

    def create_bookings(self, users, listings, count):
        """Create sample bookings."""
        bookings = []
        statuses = ['pending', 'confirmed', 'canceled', 'completed']
        
        for i in range(count):
            listing = random.choice(listings)
            user = random.choice([u for u in users if u != listing.host])
            
            # Generate random dates
            start_date = date.today() + timedelta(days=random.randint(-30, 60))
            duration = random.randint(1, 14)
            end_date = start_date + timedelta(days=duration)
            
            guests = random.randint(1, min(listing.max_guest_count, 6))
            total_price = listing.price_per_night * duration
            
            booking = Booking.objects.create(
                listing=listing,
                user=user,
                check_in_date=start_date,
                check_out_date=end_date,
                number_of_guests=guests,
                total_price=total_price,
                status=random.choice(statuses),
                special_requests=random.choice([
                    '', 'Late check-in requested', 'Extra towels please',
                    'Quiet room preferred', 'Ground floor if possible'
                ])
            )
            bookings.append(booking)
        
        return bookings

    def create_reviews(self, users, listings, count):
        """Create sample reviews."""
        reviews = []
        
        review_comments = [
            'Amazing place! Highly recommended.',
            'Great location and very clean.',
            'Perfect for a weekend getaway.',
            'Host was very responsive and helpful.',
            'Beautiful property with great amenities.',
            'Exactly as described. Will book again!',
            'Fantastic experience overall.',
            'Great value for money.',
            'Very comfortable and well-equipped.',
            'Excellent location close to everything.',
            'Clean, comfortable, and convenient.',
            'Would definitely stay here again.',
            'Perfect for families.',
            'Great host and beautiful property.',
            'Exceeded our expectations!'
        ]
        
        # Keep track of user-listing combinations to avoid duplicates
        user_listing_pairs = set()
        
        for i in range(count):
            # Try to find a unique user-listing combination
            attempts = 0
            while attempts < 50:  # Prevent infinite loop
                listing = random.choice(listings)
                user = random.choice([u for u in users if u != listing.host])
                
                pair = (user.id, listing.listing_id)
                if pair not in user_listing_pairs:
                    user_listing_pairs.add(pair)
                    break
                attempts += 1
            else:
                continue  # Skip this review if no unique pair found
            
            review = Review.objects.create(
                listing=listing,
                user=user,
                rating=random.randint(3, 5),  # Mostly good ratings
                comment=random.choice(review_comments)
            )
            reviews.append(review)
        
        return reviews