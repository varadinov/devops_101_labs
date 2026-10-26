import strawberry
from databases import Database
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from strawberry.fastapi import GraphQLRouter

# SQLite in-memory database setup
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Movie model definition
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director = Column(String, index=True)
    writer = Column(String, index=True)
    year = Column(Integer)

# Create database and tables
Base.metadata.create_all(bind=engine)

# Sample data: 10 random movies from a top 100 list
sample_movies = [
    {"title": "The Shawshank Redemption", "director": "Frank Darabont", "writer": "Stephen King", "year": 1994},
    {"title": "The Godfather", "director": "Francis Ford Coppola", "writer": "Mario Puzo", "year": 1972},
    {"title": "The Dark Knight", "director": "Christopher Nolan", "writer": "Jonathan Nolan", "year": 2008},
    {"title": "12 Angry Men", "director": "Sidney Lumet", "writer": "Reginald Rose", "year": 1957},
    {"title": "Schindler's List", "director": "Steven Spielberg", "writer": "Thomas Keneally", "year": 1993},
    {"title": "Pulp Fiction", "director": "Quentin Tarantino", "writer": "Roger Avary", "year": 1994},
    {"title": "The Good, the Bad and the Ugly", "director": "Sergio Leone", "writer": "Luciano Vincenzoni", "year": 1966},
    {"title": "Fight Club", "director": "David Fincher", "writer": "Chuck Palahniuk", "year": 1999},
    {"title": "Forrest Gump", "director": "Robert Zemeckis", "writer": "Winston Groom", "year": 1994},
    {"title": "Inception", "director": "Christopher Nolan", "writer": "Christopher Nolan", "year": 2010},
]

# Populate the database with sample data
def initialize_data():
    db = SessionLocal()
    if db.query(Movie).count() == 0:
        for movie_data in sample_movies:
            movie = Movie(**movie_data)
            db.add(movie)
        db.commit()
    db.close()

initialize_data()

# Movie GraphQL type
@strawberry.type
class MovieType:
    id: int
    title: str
    director: str
    writer: str
    year: int

# MovieFilter input type to encapsulate optional filter fields
@strawberry.input
class MovieFilter:
    year: int | None = None
    director: str | None = None
    writer: str | None = None

# Query with dynamic filtering
@strawberry.type
class Query:
    @strawberry.field
    async def movies(self, where: MovieFilter | None = None) -> list[MovieType]:
        db = SessionLocal()
        query = select(Movie)
        
        # Dynamically add filters based on fields in `where`
        if where:
            if where.year:
                query = query.where(Movie.year == where.year)
            if where.director:
                query = query.where(Movie.director == where.director)
            if where.writer:
                query = query.where(Movie.writer == where.writer)
        
        result = db.execute(query).scalars().all()
        db.close()
        return [MovieType(id=movie.id, title=movie.title, director=movie.director, writer=movie.writer, year=movie.year) for movie in result]

# Create FastAPI app and GraphQL router
schema = strawberry.Schema(query=Query)
app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")