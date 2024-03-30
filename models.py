from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import bcrypt

Base = declarative_base()
engine = create_engine('sqlite:///budget_app.db')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    main_account_balance = Column(Float, default=0.0)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    budget_accounts = relationship('BudgetAccount', back_populates='user')

class BudgetAccount(Base):
    __tablename__ = 'budget_accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='budget_accounts')
    transactions = relationship('Transaction', back_populates='account')

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # 'deposit' or 'withdrawal'
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    account_id = Column(Integer, ForeignKey('budget_accounts.id'))
    account = relationship('BudgetAccount', back_populates='transactions')

Base.metadata.create_all(engine)
