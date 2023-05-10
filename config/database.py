from sqlmodel import create_engine

sqlite_url = "sqlite:///./config/heroes.sqlite"
engine = create_engine(sqlite_url)
