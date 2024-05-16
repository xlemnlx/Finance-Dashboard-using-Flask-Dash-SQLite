from flask import current_app as server
from . import db

class Finance_Table(db.Model):
    transact_id = db.Column(db.Integer, primary_key=True)
    transact_type = db.Column(db.String(10), nullable=False)
    transact_sub_type = db.Column(db.String(100), nullable=False)
    transact_date = db.Column(db.DateTime)
    money = db.Column(db.Numeric, nullable=False)
    note = db.Column(db.String(200), nullable=True)
    
    def __repr__(self) -> str:
        return f"<Current {self.transact_id}"
    
    
    @classmethod
    def init_db(cls):
        db.create_all()

