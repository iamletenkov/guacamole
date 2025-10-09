"""Attributes endpoints for users, groups, connections."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.db.session import get_db
from app.models.guac.attributes import (
    GuacamoleConnectionAttribute,
    GuacamoleConnectionGroupAttribute,
    GuacamoleUserAttribute,
    GuacamoleUserGroupAttribute,
)

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

# Dependency injection
db_dependency = Depends(get_db)

router = APIRouter()


class AttributeSet(BaseModel):
    name: str
    value: str


class AttributeOut(BaseModel):
    name: str
    value: str


# User attributes
@router.post("/users/{user_id}/attributes", status_code=status.HTTP_201_CREATED)
def set_user_attribute(
    user_id: int, attr: AttributeSet, db: Session = db_dependency
) -> dict:
    existing = db.get(
        GuacamoleUserAttribute, {"user_id": user_id, "attribute_name": attr.name}
    )
    if existing:
        existing.attribute_value = attr.value
    else:
        new_attr = GuacamoleUserAttribute(
            user_id=user_id,
            attribute_name=attr.name,
            attribute_value=attr.value,
        )
        db.add(new_attr)
    db.commit()
    return {"status": "ok"}


@router.get("/users/{user_id}/attributes", response_model=list[AttributeOut])
def get_user_attributes(
    user_id: int, db: Session = db_dependency
) -> list[AttributeOut]:
    stmt = db.query(GuacamoleUserAttribute).filter(
        GuacamoleUserAttribute.user_id == user_id
    )
    return [
        AttributeOut(name=attr.attribute_name, value=attr.attribute_value)
        for attr in stmt.all()
    ]


@router.delete(
    "/users/{user_id}/attributes/{attr_name}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_attribute(
    user_id: int, attr_name: str, db: Session = db_dependency
) -> None:
    attr = db.get(
        GuacamoleUserAttribute, {"user_id": user_id, "attribute_name": attr_name}
    )
    if not attr:
        raise HTTPException(status_code=404, detail="Attribute not found")
    db.delete(attr)
    db.commit()


# User group attributes
@router.post(
    "/user-groups/{user_group_id}/attributes", status_code=status.HTTP_201_CREATED
)
def set_user_group_attribute(
    user_group_id: int, attr: AttributeSet, db: Session = db_dependency
) -> dict:
    existing = db.get(
        GuacamoleUserGroupAttribute,
        {"user_group_id": user_group_id, "attribute_name": attr.name},
    )
    if existing:
        existing.attribute_value = attr.value
    else:
        new_attr = GuacamoleUserGroupAttribute(
            user_group_id=user_group_id,
            attribute_name=attr.name,
            attribute_value=attr.value,
        )
        db.add(new_attr)
    db.commit()
    return {"status": "ok"}


@router.get(
    "/user-groups/{user_group_id}/attributes", response_model=list[AttributeOut]
)
def get_user_group_attributes(
    user_group_id: int, db: Session = db_dependency
) -> list[AttributeOut]:
    stmt = db.query(GuacamoleUserGroupAttribute).filter(
        GuacamoleUserGroupAttribute.user_group_id == user_group_id
    )
    return [
        AttributeOut(name=attr.attribute_name, value=attr.attribute_value)
        for attr in stmt.all()
    ]


# Connection attributes
@router.post(
    "/connections/{connection_id}/attributes", status_code=status.HTTP_201_CREATED
)
def set_connection_attribute(
    connection_id: int, attr: AttributeSet, db: Session = db_dependency
) -> dict:
    existing = db.get(
        GuacamoleConnectionAttribute,
        {"connection_id": connection_id, "attribute_name": attr.name},
    )
    if existing:
        existing.attribute_value = attr.value
    else:
        new_attr = GuacamoleConnectionAttribute(
            connection_id=connection_id,
            attribute_name=attr.name,
            attribute_value=attr.value,
        )
        db.add(new_attr)
    db.commit()
    return {"status": "ok"}


@router.get(
    "/connections/{connection_id}/attributes", response_model=list[AttributeOut]
)
def get_connection_attributes(
    connection_id: int, db: Session = db_dependency
) -> list[AttributeOut]:
    stmt = db.query(GuacamoleConnectionAttribute).filter(
        GuacamoleConnectionAttribute.connection_id == connection_id
    )
    return [
        AttributeOut(name=attr.attribute_name, value=attr.attribute_value)
        for attr in stmt.all()
    ]


# Connection group attributes
@router.post(
    "/connection-groups/{connection_group_id}/attributes",
    status_code=status.HTTP_201_CREATED,
)
def set_connection_group_attribute(
    connection_group_id: int, attr: AttributeSet, db: Session = db_dependency
) -> dict:
    existing = db.get(
        GuacamoleConnectionGroupAttribute,
        {"connection_group_id": connection_group_id, "attribute_name": attr.name},
    )
    if existing:
        existing.attribute_value = attr.value
    else:
        new_attr = GuacamoleConnectionGroupAttribute(
            connection_group_id=connection_group_id,
            attribute_name=attr.name,
            attribute_value=attr.value,
        )
        db.add(new_attr)
    db.commit()
    return {"status": "ok"}


@router.get(
    "/connection-groups/{connection_group_id}/attributes",
    response_model=list[AttributeOut],
)
def get_connection_group_attributes(
    connection_group_id: int, db: Session = db_dependency
) -> list[AttributeOut]:
    stmt = db.query(GuacamoleConnectionGroupAttribute).filter(
        GuacamoleConnectionGroupAttribute.connection_group_id == connection_group_id
    )
    return [
        AttributeOut(name=attr.attribute_name, value=attr.attribute_value)
        for attr in stmt.all()
    ]
