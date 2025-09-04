
from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Item(Base):
    """Simple ORM entity for demo CRUD operations."""
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class SQLCRUD:
    """Generic CRUD manager using SQLAlchemy ORM for a single entity type."""

    def __init__(self, db_url: str = "sqlite:///test.db") -> None:
        self.engine = create_engine(db_url, future=True)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False, class_=Session)

    def create(self, name: str) -> Item:
        """Create and persist a new Item."""
        with self.SessionLocal() as s:
            item = Item(name=name)
            s.add(item)
            s.commit()
            s.refresh(item)
            return item

    def get(self, item_id: int) -> Optional[Item]:
        """Get item by ID."""
        with self.SessionLocal() as s:
            return s.get(Item, item_id)

    def list(self) -> List[Item]:
        """List all items."""
        with self.SessionLocal() as s:
            return s.query(Item).all()

    def update(self, item_id: int, name: str) -> Optional[Item]:
        """Update item name by ID."""
        with self.SessionLocal() as s:
            obj = s.get(Item, item_id)
            if not obj:
                return None
            obj.name = name
            s.commit()
            s.refresh(obj)
            return obj

    def delete(self, item_id: int) -> bool:
        """Delete item by ID."""
        with self.SessionLocal() as s:
            obj = s.get(Item, item_id)
            if not obj:
                return False
            s.delete(obj)
            s.commit()
            return True

def main() -> None:
    crud = SQLCRUD()
    a = crud.create("alpha")
    b = crud.create("beta")
    print("List:", [i.name for i in crud.list()])
    crud.update(a.id, "alpha2")
    print("Get:", crud.get(a.id).name)
    crud.delete(b.id)
    print("List after delete:", [i.name for i in crud.list()])

if __name__ == "__main__":
    main()
