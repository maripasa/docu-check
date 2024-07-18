from db import db, Base


class CompanyModel(Base):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    cnpj = db.Column(db.CHAR(11), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)

    consultations = db.relationship("Consultation", back_populates="company")
    documents = db.relationship("CompanyDocument", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name}, cnpj={self.cnpj}, email={self.email})>"
