from app.db.session import engine
from app.db.models import Base


def init_db():
    print("✅ Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")