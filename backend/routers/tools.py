import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from database import get_db
from models import Tool, Category

router = APIRouter(prefix="/api/tools", tags=["tools"])


def tool_to_dict(t):
    d = {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "url": t.url,
        "image_url": t.image_url,
        "rating": t.rating,
        "is_featured": t.is_featured,
        "version": t.version,
        "category_name": t.category.name if t.category else None,
        "category_slug": t.category.slug if t.category else None,
        "pricing": t.pricing,
        "tags": json.loads(t.tags) if t.tags else [],
        "demo_url": t.demo_url,
        "editor_pick": t.editor_pick if hasattr(t, 'editor_pick') and t.editor_pick else False,
    }
    if hasattr(t, 'pros') and t.pros:
        d["pros"] = t.pros
    if hasattr(t, 'cons') and t.cons:
        d["cons"] = t.cons
    return d


@router.get("/featured")
def featured_tools(db: Session = Depends(get_db)):
    tools = db.query(Tool).options(joinedload(Tool.category)).filter(Tool.is_featured == True).all()
    return {"data": [tool_to_dict(t) for t in tools]}


@router.get("")
def list_tools(
    category: str = Query(None),
    pricing: str = Query(None),
    tag: str = Query(None),
    editor_pick: bool = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Tool).options(joinedload(Tool.category))

    if category:
        cat = db.query(Category).filter(Category.slug == category).first()
        if cat:
            query = query.filter(Tool.category_id == cat.id)
        else:
            return {"data": [], "total": 0, "page": page, "page_size": page_size}

    if pricing:
        query = query.filter(Tool.pricing == pricing)

    if tag:
        query = query.filter(Tool.tags.contains(tag))

    if editor_pick is not None:
        query = query.filter(Tool.editor_pick == editor_pick)

    total = query.count()
    tools = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "data": [tool_to_dict(t) for t in tools],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/editor-picks")
def editor_picks(db: Session = Depends(get_db)):
    tools = db.query(Tool).options(joinedload(Tool.category)).filter(Tool.editor_pick == True).all()
    return {"data": [tool_to_dict(t) for t in tools]}


@router.get("/search")
def search_tools(
    q: str = Query("", min_length=1),
    pricing: str = Query(None),
    tag: str = Query(None),
    editor_pick: bool = Query(None),
    db: Session = Depends(get_db),
):
    if not q.strip():
        return {"data": [], "total": 0, "query": q}

    query = (
        db.query(Tool)
        .options(joinedload(Tool.category))
        .filter(or_(Tool.name.contains(q), Tool.description.contains(q)))
    )

    if pricing:
        query = query.filter(Tool.pricing == pricing)

    if tag:
        query = query.filter(Tool.tags.contains(tag))

    if editor_pick is not None:
        query = query.filter(Tool.editor_pick == editor_pick)

    tools = query.all()

    return {"data": [tool_to_dict(t) for t in tools], "total": len(tools), "query": q}


# ── Stats (MUST be before /{tool_id}) ──

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    tool_count = db.query(func.count(Tool.id)).scalar()
    cat_count = db.query(func.count(Category.id)).scalar()
    featured_count = db.query(func.count(Tool.id)).filter(Tool.is_featured == True).scalar()
    editor_pick_count = db.query(func.count(Tool.id)).filter(Tool.editor_pick == True).scalar()
    pricing_counts = (
        db.query(Tool.pricing, func.count(Tool.id))
        .filter(Tool.pricing.isnot(None))
        .group_by(Tool.pricing)
        .all()
    )

    return {
        "data": {
            "total_tools": tool_count,
            "total_categories": cat_count,
            "featured_tools": featured_count,
            "editor_picks": editor_pick_count,
            "pricing_distribution": {p: c for p, c in pricing_counts},
        }
    }


@router.get("/{tool_id}")
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(Tool).options(joinedload(Tool.category)).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")

    related = (
        db.query(Tool)
        .filter(Tool.category_id == tool.category_id, Tool.id != tool.id)
        .limit(4)
        .all()
    )

    return {
        "data": {
            **tool_to_dict(tool),
            "pros": tool.pros,
            "cons": tool.cons,
            "pricing": tool.pricing,
            "tags": json.loads(tool.tags) if tool.tags else [],
            "screenshots": json.loads(tool.screenshots) if tool.screenshots else [],
            "created_at": tool.created_at.isoformat() if tool.created_at else None,
            "version_updated_at": tool.version_updated_at.isoformat() if tool.version_updated_at else None,
            "category": {
                "id": tool.category.id,
                "name": tool.category.name,
                "slug": tool.category.slug,
            },
            "related_tools": [
                {"id": r.id, "name": r.name, "image_url": r.image_url, "rating": r.rating}
                for r in related
            ],
        }
    }
