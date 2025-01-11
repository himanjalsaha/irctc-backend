from flask import Blueprint
from controllers.trains import add_train , check_availability, book_train , show_booking


train_routes = Blueprint('train_routes', __name__)

train_routes.route("/api/trains/create"  , methods=['POST'])(add_train)

train_routes.route("/api/trains/availability" , methods=["GET"])(check_availability)

train_routes.route("/api/train/<train_id>/book" , methods=["POST"])(book_train)

train_routes.route("/api/bookings/<booking_id>" , methods=["GET"])(show_booking)