from db import db, Base


class ConsultationModel(Base):
    __tablename__ = "consultations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    consultation_date = db.Column(db.Date, nullable=False)
    id_company = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    company = db.relationship("Company", back_populates="consultations")

    def __repr__(self):
        return f"<Consultation(id={self.id}, consultation_date={self.consultation_date}, id_company={self.id_company})>"
