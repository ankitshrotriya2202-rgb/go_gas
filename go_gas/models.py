from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)

    consumer_no = db.Column(db.String(50), unique=True)

    customer_name = db.Column(db.String(255))

    father_name = db.Column(db.String(255))

    mobile = db.Column(db.String(20))

    address = db.Column(db.Text)

    id_proof = db.Column(db.String(255))

    connection_type = db.Column(db.String(50))

    cylinder_type = db.Column(db.String(50))

    security_deposit = db.Column(db.Numeric(10,2))

    regulator_no = db.Column(db.String(255))

    stove_details = db.Column(db.String(255))

    pipe_issue_date = db.Column(db.String(255))

    email = db.Column(db.String(255))

    pan_no = db.Column(db.String(100))

    receiver_name = db.Column(db.String(255))

    cylinder_qty = db.Column(db.Integer)


class Booking(db.Model):

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    booking_no = db.Column(db.String(50))

    consumer_no = db.Column(db.String(50))

    booking_date = db.Column(db.DateTime)

    cylinder_type = db.Column(db.String(50))

    cylinder_qty = db.Column(db.Integer)

    rate = db.Column(db.Numeric(10,2))

    status = db.Column(db.String(50))
    
    payment_status = db.Column(db.String(50), default='Pending')
    
    payment_mode = db.Column(db.String(50))

    utr_no = db.Column(db.String(100))


class Delivery(db.Model):

    __tablename__ = 'deliveries'

    id = db.Column(db.Integer, primary_key=True)

    consumer_no = db.Column(db.String(50))

    delivery_date = db.Column(db.DateTime)

    filled_qty = db.Column(db.Integer)

    empty_qty = db.Column(db.Integer)

    rate = db.Column(db.Numeric(10,2))

    total_amount = db.Column(db.Numeric(10,2))

    payment_mode = db.Column(db.String(50))

    delivery_boy = db.Column(db.String(255))

    status = db.Column(db.String(50))


class Stock(db.Model):

    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)

    product_name = db.Column(db.String(100))

    filled_stock = db.Column(db.Integer)

    empty_stock = db.Column(db.Integer)