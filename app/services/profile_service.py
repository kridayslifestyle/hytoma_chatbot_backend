from sqlalchemy.orm import Session

from app.models.customer_profile import CustomerProfile

def get_profile(
        db: Session,
        customer_uid: str):

    return (

        db.query(
            CustomerProfile
        )

        .filter(

            CustomerProfile.customer_uid == customer_uid

        )

        .first()

    )

def create_profile(
        db: Session,
        customer_uid: str):

    profile = CustomerProfile(

        customer_uid=customer_uid

    )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile

def get_or_create_profile(
        db: Session,
        customer_uid: str):

    profile = get_profile(

        db,

        customer_uid

    )

    if profile:

        return profile

    return create_profile(

        db,

        customer_uid

    )

def update_budget(
        db: Session,
        customer_uid: str,
        budget: str):

    profile = get_or_create_profile(

        db,

        customer_uid

    )

    profile.budget = budget

    db.commit()

def update_profile(
        db: Session,
        customer_uid: str,
        data: dict):

    profile = get_or_create_profile(
        db,
        customer_uid
    )

    if data.get("budget"):
        profile.budget = data["budget"]

    if data.get("preferred_color"):
        profile.preferred_color = data["preferred_color"]

    if data.get("ecosystem"):
        profile.ecosystem = data["ecosystem"]

    if data.get("interests"):
        profile.interests = data["interests"]

    if data.get("location"):
        profile.location = data["location"]

    db.commit()


