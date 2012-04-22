from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from muntjac.data.util.indexed_container import IndexedContainer

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    addresses = relationship("Address", order_by="Address.id", backref="user")

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s')>" % (self.name, self.fullname)


User.__table__

ed_user = User('ed', 'Ed Jones', 'edspassword')

engine = create_engine()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

session = Session()

session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()

assert ed_user is our_user

session.add_all([
    User('wendy', 'Wendy Williams', 'foobar'),
    User('mary', 'Mary Contrary', 'xxg527'),
    User('fred', 'Fred Flinstone', 'blah')])

session.commit()

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref=backref('addresses', order_by=id))

    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return "<Address('%s')>" % self.email_address
