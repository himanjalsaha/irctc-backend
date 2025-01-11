from flask import request , jsonify
from datetime import datetime
from models.Train import Train
from utils.db import db
from utils.decorators import require_admin
from utils.generate_token import decode_token
from models.User import User
from models.Booking import Booking
@require_admin
def add_train():
 try:
    data = request.get_json()
    train_name = data.get('train_name')
    source = data.get('source')
    destination = data.get('destination')
    seat_capacity = data.get('seat_capacity')
    arrival_time_at_source = data.get('arrival_time_at_source')
    arrival_time_at_destination = data.get('arrival_time_at_destination')
    
    if not train_name or not source or not destination or not seat_capacity or not arrival_time_at_source or not arrival_time_at_destination:
            return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        arrival_time_at_source = datetime.strptime(arrival_time_at_source, '%H:%M').time()
        arrival_time_at_destination = datetime.strptime(arrival_time_at_destination, '%H:%M').time()
    except ValueError:
            return jsonify({'error': 'Invalid time format. Use HH:MM.'}), 400  
        
    train  =  Train(
            train_name=train_name,
            source=source,
            destination=destination,
            seat_capacity=seat_capacity,
            arrival_time_at_source=arrival_time_at_source,
            arrival_time_at_destination=arrival_time_at_destination
    )     
    
    db.session.add(train)
    db.session.commit()

       
    return jsonify({
            'status': 'Train added successfully',
            'train_id': train.id
        }), 201
    
 except Exception as e:
       db.session.rollback()  
       return jsonify({'error': str(e)}), 500 

    
    
    
    
def check_availability():
    source = request.args.get("source")
    destination = request.args.get("destination")   
    if not source and not destination:
        return jsonify({"error" : "source or destination is missing"}) ,  401 
    
    
    
    trains = Train.query.filter_by(source=source , destination=destination).all()
    
    train_data = [
        { "train_id": train.id,  "train_name": train.train_name, "seat_capacity": train.seat_capacity} 
        for train in trains
    ]
    
    return jsonify({"response" : train_data})



def book_train(train_id):
    data = request.get_json()
    token = request.headers.get("Authorization")
    no_of_seats = data.get("no_of_seats")
   
    
    if not token:
        return jsonify({"error": "Token is missing"}), 403
    
    if token.startswith("Bearer "):
        token = token[7:]  

    try:
       
        data = decode_token(token=token)
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({"error": "You must be a valid user to book"}), 401

        if not no_of_seats or no_of_seats <= 0:
            return jsonify({"error": "Invalid number of seats"}), 400

        train = Train.query.get(train_id)
        
        if not train:
            return jsonify({"error": "Train not found"}), 404
        
        
        existing_bookings = Booking.query.filter_by(train_id=train_id).all() #chexckinh seats that r available
        booked_seats = set()
        
        for booking in existing_bookings:
            booked_seats.update(booking.seat_numbers)

        total_seats = set(range(1, train.seat_capacity + 1))
        available_seats = sorted(total_seats - booked_seats)
        
        if len(available_seats) < no_of_seats:
            return jsonify({"error": "Not enough seats available"}), 400

        
        assigned_seats = available_seats[:no_of_seats] #asssign the seats
        
      
   
        
        
        new_booking = Booking(
            train_id=train_id,
            train_name=train.train_name,
            user_id=user.id,
            number_of_seats=no_of_seats,
            seat_numbers=assigned_seats,
            arrival_time_at_source=train.arrival_time_at_source,
            arrival_time_at_destination=train.arrival_time_at_destination
        )
        db.session.add(new_booking)
        
        
        train.seat_capacity -= no_of_seats
        db.session.commit()

        return jsonify({
            "message": "Booking successful",
            "train_name": train.train_name,
            "remaining_seats": train.seat_capacity,
            "assigned_seats": assigned_seats,
            "user": user.email
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



def show_booking(booking_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 403
    
    if token.startswith("Bearer "):
        token = token[7:]  
    
    try:
        # Decode the token
        data = decode_token(token=token)
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({"error": "You must be a valid user to access this booking"}), 401
        
        print(f"Looking for booking with ID: {booking_id}")  # Debug log
        
        booking = Booking.query.filter_by(id=booking_id).first()
        
        if not booking:
            return jsonify({"error": "Booking not found"}), 404
        
        
        arrival_time_at_source_str = booking.arrival_time_at_source.strftime('%H:%M:%S') if booking.arrival_time_at_source else None
        arrival_time_at_destination_str = booking.arrival_time_at_destination.strftime('%H:%M:%S') if booking.arrival_time_at_destination else None
        
        return jsonify({
            "message": "Booking retrieved successfully",
            "booking_id": booking.id,
            "train_id": booking.train_id,
            "train_name": booking.train_name,
            "user_id": booking.user_id,
            "number_of_seats": booking.number_of_seats,
            "seat_numbers": booking.seat_numbers,
            "arrival_time_at_source": arrival_time_at_source_str,
            "arrival_time_at_destination": arrival_time_at_destination_str
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

         

def show_booking_by_user(user_id):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 403
    
    if token.startswith("Bearer "):
        token = token[7:]  # Remove 'Bearer ' prefix  
    
    try:
        # Decode the token
        data = decode_token(token=token)
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({"error": "You must be a valid user to access this booking"}), 401
        
        print(f"Looking for bookings for user ID: {user_id}")  # Debug log
        
        bookings = Booking.query.filter_by(user_id=user_id).all()
        
        if not bookings:
            return jsonify({"error": "No bookings found for this user"}), 404
        
        bookings_data = []
        for booking in bookings:
            arrival_time_at_source_str = booking.arrival_time_at_source.strftime('%H:%M:%S') if booking.arrival_time_at_source else None
            arrival_time_at_destination_str = booking.arrival_time_at_destination.strftime('%H:%M:%S') if booking.arrival_time_at_destination else None

            bookings_data.append({
                "booking_id": booking.id,
                "train_id": booking.train_id,
                "train_name": booking.train_name,
                "user_id": booking.user_id,
                "number_of_seats": booking.number_of_seats,
                "seat_numbers": booking.seat_numbers,
                "arrival_time_at_source": arrival_time_at_source_str,
                "arrival_time_at_destination": arrival_time_at_destination_str
            })
        
        return jsonify({
            "message": "Bookings retrieved successfully",
            "bookings": bookings_data
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500