from db import db, Base

class CompanyDocument(Base):
    __tablename__ = "company_document"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    id_company = db.Column(db.ForeignKey("companies"), nullable=False)
    id_document = db.Column(db.ForeignKey("documents"), nullable=False)
    
    company = db.relationship("Company", back_populates="documents")
    document = db.relationship("Document")
    
    def __repr__(self):
        return f"<CompanyDocument(id={self.id}, start_date={self.start_date}, expiry_date={self.expiry_date}, id_company={self.id_company}, id_document={self.id_document})>"