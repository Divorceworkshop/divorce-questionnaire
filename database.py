import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    print("WARNING: DATABASE_URL environment variable is not set")
    # Use a default SQLite database as fallback (for development only)
    DATABASE_URL = "sqlite:///divorce_assessment.db"

# Configure database engine with proper connection parameters
if DATABASE_URL.startswith('postgres'):
    # For PostgreSQL, disable SSL requirement to avoid connection issues
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Test connections before using them
        pool_recycle=3600,   # Recycle connections after 1 hour
        connect_args={'sslmode': 'prefer'}  # Less strict SSL mode
    )
else:
    # For SQLite or other databases
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600
    )

# Create base class for models
Base = declarative_base()

# Define models
class AssessmentResult(Base):
    __tablename__ = "assessment_results"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    age = Column(String(50), nullable=True)
    divorce_stage = Column(String(100), nullable=True) 
    overall_score = Column(Float, nullable=False)
    legal_score = Column(Float, nullable=True)
    emotional_score = Column(Float, nullable=True)
    financial_score = Column(Float, nullable=True)
    children_score = Column(Float, nullable=True)
    recovery_score = Column(Float, nullable=True)
    responses = Column(JSON, nullable=True)  # Store all responses as JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<AssessmentResult(id={self.id}, email={self.email}, overall_score={self.overall_score})>"

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database interaction functions
def save_assessment_result(email, scores, responses):
    """
    Save assessment results to the database.
    
    Args:
        email: User's email address
        scores: Dictionary of assessment scores
        responses: Dictionary of user responses
    
    Returns:
        AssessmentResult object that was created
    """
    db = SessionLocal()
    try:
        # Create new assessment result
        result = AssessmentResult(
            email=email,
            age=responses.get('age', ''),
            divorce_stage=responses.get('divorce_stage', ''),
            overall_score=scores['overall'],
            legal_score=scores.get('legal'),
            emotional_score=scores.get('emotional'),
            financial_score=scores.get('financial'),
            children_score=scores.get('children'),
            recovery_score=scores.get('recovery'),
            responses=responses
        )
        
        # Add to session and commit
        db.add(result)
        db.commit()
        db.refresh(result)
        
        return result
    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {str(e)}")
        return None
    finally:
        db.close()

def get_assessment_results(email=None, limit=100):
    """
    Retrieve assessment results from the database.
    
    Args:
        email: Optional filter by email
        limit: Maximum number of results to return
    
    Returns:
        List of AssessmentResult objects
    """
    db = SessionLocal()
    try:
        query = db.query(AssessmentResult)
        
        if email:
            query = query.filter(AssessmentResult.email == email)
            
        results = query.order_by(AssessmentResult.created_at.desc()).limit(limit).all()
        
        return results
    except Exception as e:
        print(f"Error retrieving from database: {str(e)}")
        return []
    finally:
        db.close()
