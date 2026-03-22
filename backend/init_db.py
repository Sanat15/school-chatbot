from backend.core.database import engine, Base
from backend.models.models import *

Base.metadata.create_all(bind=engine)
print("All tables created successfully!")