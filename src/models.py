from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()
favorite_planet = Table(
    "favorite_planet",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True)
)
favorite_character = Table(
    "favorite_character",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)
favorite_vehicle = Table(
    "favorite_vehicle",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicle.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    favorite_planets = relationship("Planet", secondary=favorite_planet)
    favorite_characters = relationship("Character", secondary=favorite_character)
    favorite_vehicles = relationship("Vehicle", secondary=favorite_vehicle)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_planets": [item.serialize() for item in self.favorite_planets],
            "favorite_characters": [item.serialize() for item in self.favorite_characters],
            "favorite_vehicle": [item.serialize() for item in self.favorite_vehicle]
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = Column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
