from flask import render_template, request, redirect

from werkzeug.utils import secure_filename

import os
from models import db, Customer, Booking, Delivery, Stock

from datetime import datetime
from sqlalchemy import desc


def register_routes(app):

    # =========================
    # DASHBOARD
    # =========================

    @app.route('/')
    def dashboard():

        total_customers = Customer.query.count()

        total_bookings = Booking.query.count()

        total_deliveries = Booking.query.filter_by(
            status='Delivered'
        ).count()

        return render_template(

            'dashboard.html',

            total_customers=total_customers,

            total_bookings=total_bookings,

            total_deliveries=total_deliveries

        )



   # =========================
    # DELIVER BOOKING
    # =========================
    
    @app.route('/deliver_booking/<int:id>', methods=['GET', 'POST'])
    def deliver_booking(id):
    
        booking = Booking.query.get_or_404(id)
    
        if request.method == 'POST':
    
            booking.status = 'Delivered'
    
            booking.payment_status = 'Paid'
    
            booking.payment_mode = request.form['payment_mode']
    
            booking.utr_no = request.form['utr_no']
    
    
            # =========================
            # FILE UPLOAD
            # =========================
    
            file = request.files.get('payment_proof')
    
            if file and file.filename != '':
    
                filename = secure_filename(file.filename)
    
                upload_folder = os.path.join(
                    app.root_path,
                    'static',
                    'uploads'
                )
    
                os.makedirs(
                    upload_folder,
                    exist_ok=True
                )
    
                save_path = os.path.join(
                    upload_folder,
                    filename
                )
    
                file.save(save_path)
    
                booking.payment_proof = filename
    
                print("FILE SAVED:", filename)
    
    
            db.session.commit()
    
            return redirect('/bookings')
    
        return render_template(
    
            'deliver_booking.html',
    
            booking=booking
    
        )



    # =========================
    # CUSTOMERS
    # =========================

    @app.route('/customers')
    def customers():

        customer_list = Customer.query.all()

        return render_template(
            'customers.html',
            customers=customer_list
        )



    # =========================
    # ADD CUSTOMER
    # =========================

    @app.route('/add_customer', methods=['GET', 'POST'])
    def add_customer():

        last_customer = Customer.query.order_by(
            desc(Customer.id)
        ).first()

        if last_customer:

            last_no = int(
                last_customer.consumer_no.split('-')[1]
            )

            new_no = last_no + 1

        else:

            new_no = 1

        next_consumer_no = (
            f"DA620-{str(new_no).zfill(4)}"
        )

        if request.method == 'POST':

            customer = Customer(

                consumer_no=next_consumer_no,

                customer_name=request.form['customer_name'],

                father_name=request.form['father_name'],

                mobile=request.form['mobile'],

                address=request.form['address'],

                id_proof=request.form['id_proof'],

                connection_type=request.form['connection_type'],

                cylinder_type=request.form['cylinder_type'],

                regulator_no=request.form['regulator_no'],

                stove_details=request.form['stove_details'],

                pipe_issue_date=request.form['pipe_issue_date'],

                email=request.form['email'],

                pan_no=request.form['pan_no'],

                receiver_name=request.form['receiver_name'],

                cylinder_qty=request.form['cylinder_qty'],

                security_deposit=request.form['security_deposit']

            )

            db.session.add(customer)

            db.session.commit()

            return redirect('/customers')

        return render_template(
            'add_customer.html',
            next_consumer_no=next_consumer_no
        )



    # =========================
    # BOOKINGS
    # =========================

    @app.route('/bookings', methods=['GET', 'POST'])
    def bookings():

        now = datetime.now()

        month_year = now.strftime("%m%y")

        last_booking = Booking.query.order_by(
            desc(Booking.id)
        ).first()

        if last_booking:

            last_no = int(
                last_booking.booking_no.split('-')[-1]
            )

            new_no = last_no + 1

        else:

            new_no = 1

        next_booking_no = (
            f"BK-{month_year}-{str(new_no).zfill(4)}"
        )

        # =========================
        # SAVE BOOKING
        # =========================

        if request.method == 'POST':

            booking = Booking(

                booking_no=next_booking_no,

                consumer_no=request.form[
                    'consumer_no'
                ].strip(),

                booking_date=now,

                cylinder_type=request.form[
                    'cylinder_type'
                ],

                cylinder_qty=request.form[
                    'cylinder_qty'
                ],

                rate=request.form[
                    'rate'
                ],

                status='Pending',

                payment_status='Pending'

            )

            db.session.add(booking)

            db.session.commit()

            return redirect('/bookings')



        # =========================
        # SHOW BOOKINGS
        # =========================

        booking_list = Booking.query.order_by(
            desc(Booking.id)
        ).all()

        customers = Customer.query.order_by(
            Customer.customer_name
        ).all()

        return render_template(

            'bookings.html',

            bookings=booking_list,

            next_booking_no=next_booking_no,

            customers=customers

        )



    # =========================
    # DELIVERY
    # =========================

    @app.route('/delivery', methods=['GET', 'POST'])
    def delivery():

        if request.method == 'POST':

            filled_qty = int(
                request.form.get('filled_qty') or 0
            )

            rate = float(
                request.form.get('rate') or 0
            )

            total_amount = (
                filled_qty * rate
            )

            delivery = Delivery(

                consumer_no=request.form[
                    'consumer_no'
                ],

                delivery_date=datetime.now(),

                filled_qty=filled_qty,

                empty_qty=request.form.get(
                    'empty_qty'
                ) or 0,

                rate=rate,

                total_amount=total_amount,

                payment_mode=request.form[
                    'payment_mode'
                ],

                delivery_boy=request.form[
                    'delivery_boy'
                ],

                status='Delivered'

            )

            db.session.add(delivery)

            stock = Stock.query.first()

            if stock:

                stock.filled_stock -= filled_qty

                stock.empty_stock += int(
                    request.form.get(
                        'empty_qty'
                    ) or 0
                )

            db.session.commit()

            return redirect('/delivery')

        deliveries = Delivery.query.all()

        return render_template(
            'challan.html',
            deliveries=deliveries
        )



    # =========================
    # CONNECTION CERTIFICATE
    # =========================

    @app.route('/connection_certificate/<int:id>')
    def connection_certificate(id):

        customer = Customer.query.get_or_404(id)

        return render_template(

            'connection_certificate.html',

            customer=customer,

            current_date=datetime.now().strftime(
                '%d-%m-%Y'
            )

        )



    # =========================
    # BOOKING RECEIPT
    # =========================

    @app.route('/booking_receipt/<int:id>')
    def booking_receipt(id):

        booking = Booking.query.get_or_404(id)

        # =========================
        # CUSTOMER FETCH
        # =========================

        customer = Customer.query.filter(

            db.func.trim(
                Customer.consumer_no
            ) ==

            db.func.trim(
                booking.consumer_no
            )

        ).first()

        # =========================
        # RATE
        # =========================

        rate = float(booking.rate)

        # =========================
        # CYLINDER WEIGHT
        # =========================

        weight = float(

            booking.cylinder_type

            .replace('KG', '')

            .replace('kg', '')

            .strip()

        )

        # =========================
        # TOTAL
        # =========================

        total_amount = (

            weight *

            float(booking.cylinder_qty) *

            float(rate)

        )

        return render_template(

            'booking_receipt.html',

            booking=booking,

            customer=customer,

            rate=rate,

            total_amount=total_amount,

            current_date=datetime.now().strftime(
                '%d-%m-%Y'
            )

        )
