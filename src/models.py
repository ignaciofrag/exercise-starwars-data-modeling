import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timezone
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    subscription_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    favourite_planets = relationship('FavouritePlanet', backref='user', lazy=True)
    favourite_characters = relationship('FavouriteCharacter', backref='user', lazy=True)

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(200))
    image = Column(String(200))
    favourites = relationship('FavouriteCharacter', backref='character', lazy=True)

class Planet(Base):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(200))
    image = Column(String(200))
    favourites = relationship('FavouritePlanet', backref='planet', lazy=True)

class FavouriteCharacter(Base):
    __tablename__ = 'favourite_characters'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False)

    user = relationship('User', back_populates='favourite_characters')
    character = relationship('Character', back_populates='favourites')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id
        }

class FavouritePlanet(Base):
    __tablename__ = 'favourite_planets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    planet_id = Column(Integer, ForeignKey('planets.id'), nullable=False)

    user = relationship('User', back_populates='favourite_planets')
    planet = relationship('Planet', back_populates='favourites')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id
        }

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
