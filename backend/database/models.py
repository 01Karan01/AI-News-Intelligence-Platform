from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Table,
)

from sqlalchemy.orm import relationship

from database.database import Base


# -------------------------------------------------
# Association Tables (Many-to-Many)
# -------------------------------------------------

event_people = Table(
    "event_people",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("person_id", Integer, ForeignKey("people.id")),
)

event_organizations = Table(
    "event_organizations",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("organization_id", Integer, ForeignKey("organizations.id")),
)

event_locations = Table(
    "event_locations",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("location_id", Integer, ForeignKey("locations.id")),
)


# -------------------------------------------------
# Event Table
# -------------------------------------------------

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(500), nullable=False)

    summary = Column(Text)

    category = Column(String(100))

    confidence = Column(Integer)

    created_at = Column(DateTime)

    articles = relationship(
        "Article",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    people = relationship(
        "Person",
        secondary=event_people,
        back_populates="events",
    )

    organizations = relationship(
        "Organization",
        secondary=event_organizations,
        back_populates="events",
    )

    locations = relationship(
        "Location",
        secondary=event_locations,
        back_populates="events",
    )


# -------------------------------------------------
# Articles
# -------------------------------------------------

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(Text)

    source = Column(String(200))

    url = Column(Text)

    published_at = Column(DateTime)

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
    )

    event = relationship(
        "Event",
        back_populates="articles",
    )


# -------------------------------------------------
# People
# -------------------------------------------------

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), unique=True)

    events = relationship(
        "Event",
        secondary=event_people,
        back_populates="people",
    )


# -------------------------------------------------
# Organizations
# -------------------------------------------------

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), unique=True)

    events = relationship(
        "Event",
        secondary=event_organizations,
        back_populates="organizations",
    )


# -------------------------------------------------
# Locations
# -------------------------------------------------

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), unique=True)

    events = relationship(
        "Event",
        secondary=event_locations,
        back_populates="locations",
    )