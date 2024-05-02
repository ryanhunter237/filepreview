from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class File(db.Model):
    __tablename__ = "file"

    groupid: str = db.Column(db.String(32), primary_key=True, nullable=False)
    filepath: str = db.Column(db.String, primary_key=True, nullable=False)
    md5: str = db.Column(db.String(32), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<File groupid={self.groupid}, filepath={self.filepath}, md5={self.md5}>"
        )
