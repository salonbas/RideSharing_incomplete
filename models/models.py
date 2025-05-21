# === 建立必要檔案與範本 ===
# 以下為你應建立的目錄與檔案，含初始程式碼結構與註解：

# models/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

user_event_association = Table(
    "user_event_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    nickname = Column(String)
    avatarUrl = Column(String)
    instagram = Column(String)
    email = Column(String)
    phone = Column(String)
    bio = Column(String)

    events = relationship("Event", back_populates="organizer")
    joined_events = relationship("Event", secondary=user_event_association, back_populates="participants")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "avatarUrl": self.avatarUrl,
            "instagram": self.instagram,
            "email": self.email,
            "phone": self.phone,
            "bio": self.bio,
        }



class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    type = Column(String)
    date = Column(DateTime)
    requiredSeats = Column(Integer)
    joinedSeats = Column(Integer)
    organizer_id = Column(Integer, ForeignKey("users.id"))
    organizer = relationship("User", back_populates="events")
    participants = relationship("User", secondary=user_event_association, back_populates="joined_events")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "date": self.date.isoformat(),
            "requiredSeats": self.requiredSeats,
            "joinedSeats": self.joinedSeats,
            "organizer": {
                "id": self.organizer.id,
                "nickname": self.organizer.nickname,
                "avatarUrl": self.organizer.avatarUrl,
            }
        }