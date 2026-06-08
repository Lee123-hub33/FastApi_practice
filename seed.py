from dotenv import load_dotenv
load_dotenv()  # Forces system execution environment to read .env first!

import os
from sqlalchemy.orm import Session
from app.database import sessionLocal, engine, Base
from app import models

mock_tasks = [
    {"title": "Design centralized database schema", "description": "Drafting tables for the core platform."},
    {"title": "Optimize pipeline throughput", "description": "Reviewing execution logs to locate data bottlenecks."},
    {"title": "Configure cloud infrastructure", "description": "Setting up local Docker runtime targets."},
    {"title": "Review data validation schemas", "description": "Inspecting Pydantic models for tracking events."},
    {"title": "Automate contract parsing pipeline", "description": "Writing logic to extract text elements from files."}
]

def seed_database():
    print("🚀 Starting the database seeding pipeline...")
    db: Session = sessionLocal()

    try:
        existing_count = db.query(models.Task).count()
        if existing_count > 0:
            print(f"⚠️ Database already contains {existing_count} tasks. Skipping seeding.")
            return

        print(f"📦 Staging {len(mock_tasks)} mock records...")
        for task_dict in mock_tasks:
            db_task = models.Task(**task_dict)
            db.add(db_task)

        db.commit()
        print("✅ Bulk data insertion completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ An error occurred during database seeding: {e}")

    finally:
        db.close()
        print("🔒 Database connection safely closed.")

if __name__ == "__main__":
    seed_database()