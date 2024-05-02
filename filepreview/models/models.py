from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class File(db.Model):
    __tablename__ = "file"

    # an identifier for groups of files
    group_id: str = db.Column(db.String(32), primary_key=True, nullable=False)
    # The path of the file, relative to some parent directory
    # which is the same for files with the same group_id.
    file_path: str = db.Column(db.String, primary_key=True, nullable=False)
    # md5 hash of the file's contents
    md5: str = db.Column(db.String(32), nullable=False)

    def __repr__(self) -> str:
        return f"<File group_id={self.group_id}, file_path={self.file_path}, md5={self.md5}>"


class FileData(db.Model):
    __tablename__ = "filedata"

    # md5 hash identifying a file's contents
    md5: str = db.Column(db.String(32), primary_key=True, nullable=False)
    # the size of the file in bytes
    num_bytes: int = db.Column(db.Integer, nullable=False)
    # the absolute path where the file is saved on the local filesystem
    local_path: str = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<FileData md5={self.md5}, num_bytes={self.num_bytes}, local_path={self.local_path}>"
