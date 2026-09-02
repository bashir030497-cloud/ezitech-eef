from app.db.database import Base, engine
from app.core.logger import get_logger

# Import all models so they register with Base before create_all
from app.models import submission, evaluation, score, test_result, leaderboard  # noqa

logger = get_logger("init_db")


def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")


if __name__ == "__main__":
    init_db()
