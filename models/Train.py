from utils.db import db
import uuid
class Train(db.Model):
    id = db.Column(db.String(400), primary_key=True , default=lambda: str(uuid.uuid4()))
    train_name = db.Column(db.String(80), nullable=False)
    source = db.Column(db.String(120),  nullable=False)
    destination = db.Column(db.String(120),  nullable=False)
    seat_capacity = db.Column(db.Integer,  nullable=False)
    arrival_time_at_source = db.Column(db.Time, nullable=False)
    arrival_time_at_destination = db.Column(db.Time,  nullable=False)
    