from db import db, Base


class DocumentModel(Base):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.VARCHAR(255), nullable=False)

    def __repr__(self):
        return f"<Document(id={self.id}, type={self.type})>"
