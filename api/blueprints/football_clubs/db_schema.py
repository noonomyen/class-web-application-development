from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class FootballBase(DeclarativeBase):
    __tablename__: str

# Enumerate Tables

class Nationality(FootballBase):
    __tablename__ = "nationalities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)

class PlayerPosition(FootballBase):
    __tablename__ = "player_positions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))

# Data Tables

class Club(FootballBase):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256), unique=True)
    image_url: Mapped[str] = mapped_column(String(2048))

    players: Mapped[List["Player"]] = relationship("Player", back_populates="club", cascade="all, delete-orphan")

class Player(FootballBase):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(256))
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey("clubs.id"))
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey("player_positions.id"))
    nationality_id: Mapped[int] = mapped_column(Integer, ForeignKey("nationalities.id"))
    image_url: Mapped[str] = mapped_column(String(2024))

    club: Mapped[Club] = relationship("Club", back_populates="players")
    position: Mapped[PlayerPosition] = relationship("PlayerPosition")
    nationality: Mapped[Nationality] = relationship("Nationality")
