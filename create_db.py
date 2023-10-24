from db import Base, engine

print("Creating database...")

Base.metadata.create_all(bind=engine)
