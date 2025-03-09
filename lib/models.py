from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id', name="fk_auditions_role_id_roles"))

    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    auditions = relationship("Audition", back_populates="role")

    def role_auditions(self):
        return self.auditions

    def role_actors(self):
        return [audition.actor for audition in self.auditions]

    def role_locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        return next((audition for audition in self.auditions if audition.hired), None)

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return next((audition for audition in hired_auditions if audition != self.lead()), None)

# Setup the database
engine = create_engine('sqlite:///theater.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
