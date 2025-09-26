from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()
# Relationship tables
favorite_planet = Table(
    "favorite_planet",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey(
        "user.id", ondelete='CASCADE'), primary_key=True),
    Column("planet_id", ForeignKey("planet.id",
           ondelete='CASCADE'), primary_key=True)
)
favorite_character = Table(
    "favorite_character",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey(
        "user.id", ondelete='CASCADE'), primary_key=True),
    Column("character_id", ForeignKey(
        "character.id", ondelete='CASCADE'), primary_key=True)
)
favorite_vehicle = Table(
    "favorite_vehicle",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey(
        "user.id", ondelete='CASCADE'), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicle.id",
           ondelete='CASCADE'), primary_key=True)
)

# Main tables


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    favorite_planets = relationship(
        "Planet", secondary=favorite_planet, back_populates="favorited_by"
    )
    favorite_characters = relationship(
        "Character", secondary=favorite_character, back_populates="favorited_by"
    )
    favorite_vehicles = relationship(
        "Vehicle", secondary=favorite_vehicle, back_populates="favorited_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_planets": [item.serialize() for item in self.favorite_planets],
            "favorite_characters": [item.serialize() for item in self.favorite_characters],
            "favorite_vehicles": [item.serialize() for item in self.favorite_vehicles]
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    favorited_by = relationship(
        "User", secondary=favorite_planet, back_populates="favorite_planets"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    favorited_by = relationship(
        "User", secondary=favorite_character, back_populates="favorite_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    favorited_by = relationship(
        "User", secondary=favorite_vehicle, back_populates="favorite_vehicles"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
