from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

sql_database = "sqlite:///new_users.db"

engine = create_engine(sql_database)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    # one to one
    password = relationship('Password', back_populates="user", uselist=False)

    # one to many
    books = relationship('Book', back_populates="owner")

    # many to many
    subscriptions = relationship('Subscription', back_populates="users", secondary='user_sub')

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, age={self.age})>"


class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)

    user = relationship('User', back_populates="password")

    def __repr__(self):
        return f"<Password(id={self.id}, user={self.user}, password={self.password})>"


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, name={self}, owner={self}"


user_sub = Table(
    'user_sub', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('sub_id', Integer, ForeignKey('subscription.id'))
)


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship('User', secondary='user_sub', back_populates="subscriptions")

    def __repr__(self):
        return f"<Subscription(id={self.id}, name={self}, users={self.users})>"


class Item(db.Model):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    description: Mapped[str] = mapped_column(db.String(200), nullable=False)


def create_table(app):
    with app.app_context():
        db.create_all()


def fill(app):
    with app.app_context():
        user = User(name="<NAME>", email="<EMAIL>")
        db.session.add(user)
        db.session.commit()
