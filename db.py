import sqlalchemy
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)

db = sqlalchemy
engine = db.create_engine("postgresql+psycopg2://postgres:postgres@localhost/docucheck")
Session = sessionmaker(bind=engine)
Base = declarative_base()
