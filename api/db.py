from flask_sqlalchemy import SQLAlchemy
from api.blueprints.football_clubs.db_schema import FootballBase

__all__ = ["football_clubs_db"]

football_clubs_db = SQLAlchemy(model_class=FootballBase)
