from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Category

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"data": [{"id": c.id, "name": c.name, "slug": c.slug, "description": c.description, "icon": c.icon} for c in categories]}


@router.get("/{slug}")
def get_category(slug: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.slug == slug).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    tools = [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "url": t.url,
            "image_url": t.image_url,
            "rating": t.rating,
            "is_featured": t.is_featured,
            "version": t.version,
        }
        for t in category.tools
    ]

    return {
        "data": {
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "icon": category.icon,
            "tools": tools,
        }
    }
