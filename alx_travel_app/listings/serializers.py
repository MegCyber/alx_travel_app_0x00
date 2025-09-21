"""
Serializers for the ALX Travel App listings API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model (for nested representation).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'listing', 'user', 'user_id', 'rating', 
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['review_id', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        """Validate that rating is between 1 and 5."""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model.
    """
    host = UserSerializer(read_only=True)
    host_id = serializers.IntegerField(write_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    amenities_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'location', 
            'price_per_night', 'number_of_bedrooms', 'number_of_bathrooms',
            'max_guest_count', 'host', 'host_id', 'created_at', 'updated_at',
            'is_available', 'amenities', 'amenities_list', 'reviews', 
            'average_rating'
        ]
        read_only_fields = ['listing_id', 'created_at', 'updated_at']
    
    def get_amenities_list(self, obj):
        """Convert comma-separated amenities string to list."""
        if obj.amenities:
            return [amenity.strip() for amenity in obj.amenities.split(',')]
        return []
    
    def validate_price_per_night(self, value):
        """Validate that price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be positive.")
        return value
    
    def validate_max_guest_count(self, value):
        """Validate that max guest count is at least 1."""
        if value < 1:
            raise serializers.ValidationError("Maximum guest count must be at least 1.")
        return value


class ListingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing lists (without nested reviews).
    """
    host = UserSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.SerializerMethodField()
    amenities_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'location', 
            'price_per_night', 'number_of_bedrooms', 'number_of_bathrooms',
            'max_guest_count', 'host', 'is_available', 'amenities_list',
            'average_rating', 'review_count', 'created_at'
        ]
    
    def get_review_count(self, obj):
        """Get the number of reviews for this listing."""
        return obj.reviews.count()
    
    def get_amenities_list(self, obj):
        """Convert comma-separated amenities string to list."""
        if obj.amenities:
            return [amenity.strip() for amenity in obj.amenities.split(',')]
        return []


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model.
    """
    listing = ListingListSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'listing_id', 'user', 'user_id',
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_price', 'status', 'special_requests', 'duration_days',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['booking_id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Custom validation for booking data."""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_in and check_out:
            if check_out <= check_in:
                raise serializers.ValidationError(
                    "Check-out date must be after check-in date."
                )
        
        # Validate number of guests against listing capacity
        listing_id = data.get('listing_id')
        number_of_guests = data.get('number_of_guests')
        
        if listing_id and number_of_guests:
            try:
                listing = Listing.objects.get(listing_id=listing_id)
                if number_of_guests > listing.max_guest_count:
                    raise serializers.ValidationError(
                        f"Number of guests ({number_of_guests}) exceeds "
                        f"maximum allowed ({listing.max_guest_count})."
                    )
            except Listing.DoesNotExist:
                raise serializers.ValidationError("Invalid listing ID.")
        
        return data
    
    def validate_total_price(self, value):
        """Validate that total price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Total price must be positive.")
        return value


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating bookings.
    """
    class Meta:
        model = Booking
        fields = [
            'listing_id', 'check_in_date', 'check_out_date',
            'number_of_guests', 'special_requests'
        ]
    
    def validate(self, data):
        """Custom validation for booking creation."""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        
        return data