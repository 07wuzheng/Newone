from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pydantic import BaseModel, field_validator
from urllib.parse import urlparse
from database import Base, get_db
from models import Category

router = APIRouter(prefix="/api/tools", tags=["submissions"])


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    image_url = Column(String(500), nullable=True)
    status = Column(String(20), default="pending_review")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SubmitInput(BaseModel):
    name: str
    description: str
    url: str
    category_id: int

    @field_validator("name")
    @classmethod
    def name_length(cls, v):
        if len(v) < 2 or len(v) > 100:
            raise ValueError("名称长度应在 2-100 字符之间")
        return v

    @field_validator("description")
    @classmethod
    def desc_length(cls, v):
        if len(v) < 10 or len(v) > 500:
            raise ValueError("描述长度应在 10-500 字符之间")
        return v

    @field_validator("url")
    @classmethod
    def valid_url(cls, v):
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("请输入合法的网址（以 http:// 或 https:// 开头）")
        return v


def _get_logo_url(tool_url: str) -> str:
    """Build a DuckDuckGo favicon URL from a tool's URL."""
    domain = urlparse(tool_url).netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return f"https://icons.duckduckgo.com/ip3/{domain}.ico"


@router.post("/submit", status_code=201)
def submit_tool(input_data: SubmitInput, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == input_data.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="分类不存在")

    submission = Submission(
        name=input_data.name,
        description=input_data.description,
        url=input_data.url,
        category_id=input_data.category_id,
        image_url=_get_logo_url(input_data.url),
    )
    db.add(submission)
    db.commit()

    return {"data": {"id": submission.id, "status": "pending_review"}, "message": "提交成功，审核后将会展示"}
