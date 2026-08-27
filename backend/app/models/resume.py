from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, 
        ForeignKey("users.id"),
        nullable=False,
        index = True
        )

    filename = Column(String, nullable=False)
    file_path = Column(Text, nullable=False)

    parsed_text = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)
    
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default = func.now(),
        onupdate = func.now(),
        nullable = False    
    )





