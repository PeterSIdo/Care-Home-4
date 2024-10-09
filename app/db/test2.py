from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class FluidChart(Base):
    __tablename__ = 'fluid_chart'
    id = Column(Integer, primary_key=True)
    resident_initials = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    fluid_type = Column(String)
    fluid_volume = Column(Integer)
    fluid_note = Column(String)
    staff_initials = Column(String)

def connect_to_db():
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

def insert_test_data():
    Session = connect_to_db()
    session = Session()
    try:
        new_entry = FluidChart(
            resident_initials='JD',
            fluid_type='Water',
            fluid_volume=250,
            fluid_note='Morning intake',
            staff_initials='AB'
        )
        session.add(new_entry)
        session.commit()
    finally:
        session.close()