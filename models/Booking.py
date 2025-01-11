from utils.db import db
import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import JSON

class Booking(db.Model):
    id = db.Column(db.String(400), primary_key=True, default=lambda: str(uuid.uuid4()))
    train_id = db.Column(db.String(400), nullable=False)
    train_name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.String(400), nullable=False)
    number_of_seats = db.Column(db.Integer, nullable=False)
    seat_numbers = db.Column(JSON, nullable=False)  
    arrival_time_at_source = db.Column(db.Time, nullable=False)
    arrival_time_at_destination = db.Column(db.Time, nullable=False)
