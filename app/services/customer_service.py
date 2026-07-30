import uuid

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.customer_channel import CustomerChannel

def create_customer(
        db: Session,
        name: str = None):

    customer_uid = str(
        uuid.uuid4()
    )

    customer = Customer(

        customer_uid=customer_uid,

        name=name
    )

    db.add(customer)

    db.commit()

    db.refresh(customer)

    return customer

def link_channel(
        db: Session,
        customer_uid: str,
        platform: str,
        platform_user_id: str):

    channel = CustomerChannel(

        customer_uid=customer_uid,

        platform=platform,

        platform_user_id=platform_user_id
    )

    db.add(channel)

    db.commit()

    return channel

def get_customer_by_channel(
        db: Session,
        platform: str,
        platform_user_id: str):

    channel = (

        db.query(
            CustomerChannel
        )

        .filter(

            CustomerChannel.platform == platform,

            CustomerChannel.platform_user_id == platform_user_id

        )

        .first()

    )

    if channel:

        customer = (

            db.query(
                Customer
            )

            .filter(

                Customer.customer_uid == channel.customer_uid

            )

            .first()

        )

        return customer

    return None

def get_or_create_customer(
        db: Session,
        platform: str,
        platform_user_id: str,
        name: str = None):

    customer = get_customer_by_channel(
        db,
        platform,
        platform_user_id
    )

    # Existing customer
    if customer:

        return customer

    # Create new customer
    customer = create_customer(
        db,
        name
    )

    # Link platform account
    link_channel(
        db,
        customer.customer_uid,
        platform,
        platform_user_id
    )

    return customer

