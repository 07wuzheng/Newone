from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(200), nullable=True)
    icon = Column(String(50), nullable=True)

    tools = relationship("Tool", back_populates="category")


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    image_url = Column(String(500), nullable=True)
    rating = Column(Float, default=0.0)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    version = Column(String(50), nullable=True)
    version_updated_at = Column(DateTime, nullable=True)

    # New fields v2
    pricing = Column(String(20), nullable=True)       # free / freemium / paid
    tags = Column(Text, nullable=True)                 # JSON array
    pros = Column(Text, nullable=True)
    cons = Column(Text, nullable=True)
    screenshots = Column(Text, nullable=True)          # JSON array of URLs
    demo_url = Column(String(500), nullable=True)       # 演示图片/GIF URL
    editor_pick = Column(Boolean, default=False)

    category = relationship("Category", back_populates="tools")
