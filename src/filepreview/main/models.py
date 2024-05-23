from pathlib import PurePath

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class File(db.Model):
    __tablename__ = "file"

    # an identifier for groups of files
    group_id: str = db.Column(db.String(32), primary_key=True, nullable=False)
    # The directory where the file is located, relative to a parent directory
    # which is the same for files with the same group_id.
    directory: str = db.Column(db.String, primary_key=True, nullable=False)
    filename: str = db.Column(db.String, primary_key=True, nullable=False)
    # md5 hash of the file's contents
    md5: str = db.Column(db.String(32), nullable=False)

    @validates("group_id", "md5")
    def make_lowercase(self, key, value: str):
        if value:
            return value.lower()
        return value

    @validates("directory")
    def make_posix(self, key, path: str):
        path = path or ""
        return PurePath(path).as_posix()

    def __repr__(self) -> str:
        return f"<File group_id={self.group_id}, directory={self.directory}, filename={self.filename}, md5={self.md5}>"


class FileData(db.Model):
    __tablename__ = "filedata"

    # md5 hash identifying a file's contents
    md5: str = db.Column(db.String(32), primary_key=True, nullable=False)
    # the size of the file in bytes
    num_bytes: int = db.Column(db.Integer, nullable=False)
    # the absolute path where the file is saved on the local filesystem
    local_path: str = db.Column(db.String, nullable=False)
    # the name of the program for opening the file
    program: str = db.Column(db.String, nullable=True)

    @validates("md5")
    def make_lowercase(self, key, value: str):
        if value:
            return value.lower()
        return value

    @validates("local_path")
    def make_posix(self, key, path: str):
        if path:
            return PurePath(path).as_posix()
        return path

    def __repr__(self) -> str:
        return f"<FileData md5={self.md5}, num_bytes={self.num_bytes}, local_path={self.local_path}>"


class Program(db.Model):
    __tablename__ = "program"

    # the name of the program
    name: str = db.Column(db.String, primary_key=True, nullable=False)
    # the executable needed to run the program
    executable: str = db.Column(db.String, nullable=False)

    @validates("executable")
    def make_posix(self, key, path: str):
        if path:
            return PurePath(path).as_posix()
        return path

    def __repr__(self) -> str:
        return f"<Program name={self.name}, executable={self.executable}"


class Thumbnail(db.Model):
    __tablename__ = "thumbnail"

    # md5 hash identifying a file's contents
    md5: str = db.Column(db.String(32), primary_key=True, nullable=False)
    # the order to display the thumbnails in
    order: int = db.Column(db.Integer, primary_key=True, nullable=False)
    # the absolute path where the thumbnail is saved on the local filesystem
    path: str = db.Column(db.String, nullable=False)

    @validates("md5")
    def make_lowercase(self, key, value: str):
        if value:
            return value.lower()
        return value

    @validates("path")
    def make_posix(self, key, path: str):
        if path:
            return PurePath(path).as_posix()
        return path

    def __repr__(self) -> str:
        return f"<Thumbnail md5={self.md5}, order={self.order}, path={self.path}>"


class Image(db.Model):
    __tablename__ = "image"

    # md5 hash identifying a file's contents
    md5: str = db.Column(db.String(32), primary_key=True, nullable=False)
    # the order to display the thumbnails in
    order: int = db.Column(db.Integer, primary_key=True, nullable=False)
    # the absolute path where the thumbnail is saved on the local filesystem
    path: str = db.Column(db.String, nullable=False)

    @validates("md5")
    def make_lowercase(self, key, value: str):
        if value:
            return value.lower()
        return value

    @validates("path")
    def make_posix(self, key, path: str):
        if path:
            return PurePath(path).as_posix()
        return path
