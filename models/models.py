# === 建立必要檔案與範本 ===
# 以下為你應建立的目錄與檔案，含初始程式碼結構與註解：

# models/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class EventParticipant(Base):
    __tablename__ = "event_participants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # 確保同一個用戶不能重複參加同一個活動
    __table_args__ = (UniqueConstraint('event_id', 'user_id'),)
    
    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="joined_events")

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
    joined_events = relationship("EventParticipant", back_populates="user")

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
        
    def to_public_dict(self):
        return {
            "nickname": self.nickname or self.username,  # 沒有 nickname 就用 username
            "avatarUrl": self.avatarUrl,
            "instagram": self.instagram,
            "phone": self.phone,
            "bio": self.bio
        }


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    type = Column(String)
    date = Column(DateTime)
    requiredSeats = Column(Integer)
    joinedSeats = Column(Integer, default=0)  # 建議加上預設值
    organizer_id = Column(Integer, ForeignKey("users.id"))
    from_city = Column(String)
    from_detail = Column(String)
    to_city = Column(String)
    to_detail = Column(String)
    contact_method = Column(String)  
    price = Column(Integer, default=0)

    organizer = relationship("User", back_populates="events")
    participants = relationship("EventParticipant", back_populates="event")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "date": self.date.isoformat(),
            "requiredSeats": self.requiredSeats,
            "joinedSeats": self.joinedSeats,
            "spotsRemaining": self.requiredSeats - self.joinedSeats,
            "contactMethod": self.contact_method,  
            "price": self.price,
            "organizer": {
                "id": self.organizer.id,
                "nickname": self.organizer.nickname,
                "avatarUrl": self.organizer.avatarUrl,
            },
            "location": {
                "from": {
                    "city": self.from_city,
                    "detail": self.from_detail
                },
                "destination": {
                    "city": self.to_city,
                    "detail": self.to_detail
                }
            }
        }