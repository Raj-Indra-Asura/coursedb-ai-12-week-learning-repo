"""
Learning Navigation Service

Manages the unified learning system with progressive navigation
across all 12 weeks of the course repository.

Features:
- Week discovery and indexing
- Resource file discovery
- Progressive navigation (prev/next week)
- Learning path management
- Progress tracking

Learning Objectives:
- Build a unified navigation system
- Enable seamless traversal across curriculum
- Integrate filesystem with database
- Track learning progress
"""

from pathlib import Path

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import LearningResource, LearningWeek
from app.schemas import CurriculumOverviewResponse, LearningWeekResponse, NavigationResponse


class LearningNavigationService:
    """
    Service for managing learning navigation and curriculum structure
    """

    def __init__(self, repo_root: str | None = None):
        # Derive the repository root from this file's location so the service
        # works regardless of the checkout path (local, CI, container). The
        # service lives at <repo>/app/services/, so the root is two parents up.
        if repo_root is None:
            self.repo_root = Path(__file__).resolve().parents[2]
        else:
            self.repo_root = Path(repo_root)
        self.weeks_dir = self.repo_root / "weeks"

        # Week metadata mapping
        self.week_metadata = {
            1: {"title": "DBMS Foundations + Project Orientation", "status": "completed"},
            2: {"title": "SQL Basics Through Academic Data", "status": "completed"},
            3: {"title": "ER Modeling + Schema Design", "status": "completed"},
            4: {"title": "Functional Dependencies + Normalization", "status": "completed"},
            5: {"title": "PostgreSQL + FastAPI Foundation", "status": "completed"},
            6: {"title": "SQL Queries, Views, Triggers, Constraints", "status": "completed"},
            7: {"title": "Indexing, B+ Tree, Hashing", "status": "completed"},
            8: {"title": "Query Optimization + EXPLAIN", "status": "completed"},
            9: {"title": "Transactions, ACID, Concurrency", "status": "completed"},
            10: {"title": "Embeddings, pgvector, Semantic Search", "status": "completed"},
            11: {"title": "Integrated CourseDB-AI System", "status": "completed"},
            12: {"title": "Evaluation, Polish, Portfolio", "status": "completed"},
        }

        # Resource type mapping by file pattern
        self.resource_type_map = {
            "README.md": "documentation",
            "theory_notes.md": "documentation",
            "implementation_plan.md": "documentation",
            "exercises.md": "exercise",
            "checkpoints.md": "exercise",
            "solutions.md": "solution",
            "reflection.md": "reflection",
            "mistakes_to_expect.md": "documentation",
            ".ipynb": "notebook",
            ".py": "code",
            ".sql": "code",
        }

    def discover_weeks(self) -> list[dict]:
        """
        Discover all week directories in the repository

        Returns:
            List of week metadata dictionaries
        """
        weeks = []

        if not self.weeks_dir.exists():
            return weeks

        for week_dir in sorted(self.weeks_dir.iterdir()):
            if not week_dir.is_dir() or not week_dir.name.startswith("week_"):
                continue

            # Extract week number from directory name (e.g., week_01_dbms_foundations -> 1)
            try:
                week_num = int(week_dir.name.split("_")[1])
            except (IndexError, ValueError):
                continue

            if week_num < 1 or week_num > 12:
                continue

            # Get metadata for this week
            metadata = self.week_metadata.get(week_num, {})
            title = metadata.get("title", f"Week {week_num}")
            status = metadata.get("status", "not_started")

            # Try to extract description from README
            description = self._extract_description(week_dir)

            weeks.append(
                {
                    "week_number": week_num,
                    "title": title,
                    "description": description,
                    "directory_path": str(week_dir.relative_to(self.repo_root)),
                    "status": status,
                    "absolute_path": str(week_dir),
                }
            )

        return sorted(weeks, key=lambda w: w["week_number"])

    def _extract_description(self, week_dir: Path) -> str | None:
        """
        Extract description from week README file

        Args:
            week_dir: Path to week directory

        Returns:
            Description text or None
        """
        readme_path = week_dir / "README.md"
        if not readme_path.exists():
            return None

        try:
            with open(readme_path, encoding="utf-8") as f:
                content = f.read()
                # Look for "Why This Week Matters" or first paragraph
                if "## 🎯 Why This Week Matters" in content:
                    lines = content.split("\n")
                    in_section = False
                    description_lines = []
                    for line in lines:
                        if "## 🎯 Why This Week Matters" in line:
                            in_section = True
                            continue
                        if in_section:
                            if line.startswith("##") or line.startswith("---"):
                                break
                            if line.strip():
                                description_lines.append(line.strip())
                    return " ".join(description_lines[:3])  # First 3 lines

                # Fallback: get first non-empty paragraph
                lines = [
                    ln.strip() for ln in content.split("\n") if ln.strip() and not ln.startswith("#")
                ]
                return lines[0] if lines else None
        except Exception:
            return None

    def discover_resources(self, week_dir: Path) -> list[dict]:
        """
        Discover all learning resources in a week directory

        Args:
            week_dir: Path to week directory

        Returns:
            List of resource metadata dictionaries
        """
        resources = []

        if not week_dir.exists():
            return resources

        # Scan directory for learning resources
        order = 0
        for item in sorted(week_dir.rglob("*")):
            if not item.is_file():
                continue

            # Determine resource type
            resource_type = self._get_resource_type(item)
            if not resource_type:
                continue

            # Get title from filename
            title = self._get_resource_title(item)

            resources.append(
                {
                    "title": title,
                    "file_path": str(item.relative_to(self.repo_root)),
                    "resource_type": resource_type,
                    "description": None,
                    "order_index": order,
                    "absolute_path": str(item),
                }
            )
            order += 1

        return resources

    def _get_resource_type(self, file_path: Path) -> str | None:
        """
        Determine resource type from file name/extension

        Args:
            file_path: Path to file

        Returns:
            Resource type string or None
        """
        filename = file_path.name

        # Check exact filename matches
        for pattern, rtype in self.resource_type_map.items():
            if filename == pattern:
                return rtype

        # Check extension matches
        for pattern, rtype in self.resource_type_map.items():
            if pattern.startswith(".") and filename.endswith(pattern):
                return rtype

        return None

    def _get_resource_title(self, file_path: Path) -> str:
        """
        Generate human-readable title from filename

        Args:
            file_path: Path to file

        Returns:
            Formatted title
        """
        filename = file_path.stem
        # Convert underscores to spaces and title case
        title = filename.replace("_", " ").title()
        return title

    def initialize_curriculum(self, db: Session) -> list[LearningWeek]:
        """
        Initialize the learning curriculum in the database
        Discovers all weeks and their resources

        Args:
            db: Database session

        Returns:
            List of created LearningWeek objects
        """
        # Discover all weeks
        weeks_data = self.discover_weeks()
        created_weeks = []

        for week_data in weeks_data:
            # Check if week already exists
            existing_week = (
                db.query(LearningWeek)
                .filter(LearningWeek.week_number == week_data["week_number"])
                .first()
            )

            if existing_week:
                # Update existing week
                existing_week.title = week_data["title"]
                existing_week.description = week_data["description"]
                existing_week.status = week_data["status"]
                week = existing_week
            else:
                # Create new week
                week = LearningWeek(
                    week_number=week_data["week_number"],
                    title=week_data["title"],
                    description=week_data["description"],
                    directory_path=week_data["directory_path"],
                    status=week_data["status"],
                )
                db.add(week)

            db.flush()  # Get week_id

            # Discover and add resources for this week
            week_dir = Path(week_data["absolute_path"])
            resources_data = self.discover_resources(week_dir)

            for resource_data in resources_data:
                # Check if resource already exists
                existing_resource = (
                    db.query(LearningResource)
                    .filter(
                        LearningResource.week_id == week.week_id,
                        LearningResource.file_path == resource_data["file_path"],
                    )
                    .first()
                )

                if not existing_resource:
                    resource = LearningResource(
                        week_id=week.week_id,
                        title=resource_data["title"],
                        file_path=resource_data["file_path"],
                        resource_type=resource_data["resource_type"],
                        description=resource_data["description"],
                        order_index=resource_data["order_index"],
                    )
                    db.add(resource)

            created_weeks.append(week)

        db.commit()
        return created_weeks

    def get_week_by_number(self, db: Session, week_number: int) -> LearningWeek | None:
        """
        Get week by week number with all resources

        Args:
            db: Database session
            week_number: Week number (1-12)

        Returns:
            LearningWeek object or None
        """
        return db.query(LearningWeek).filter(LearningWeek.week_number == week_number).first()

    def get_navigation(self, db: Session, week_number: int) -> NavigationResponse | None:
        """
        Get navigation context for a specific week (current, prev, next)

        Args:
            db: Database session
            week_number: Current week number

        Returns:
            NavigationResponse or None if week not found
        """
        current_week = self.get_week_by_number(db, week_number)
        if not current_week:
            return None

        # Get previous week
        previous_week = None
        if week_number > 1:
            previous_week = self.get_week_by_number(db, week_number - 1)

        # Get next week
        next_week = None
        if week_number < 12:
            next_week = self.get_week_by_number(db, week_number + 1)

        # Calculate progress
        total_weeks = 12
        completed_count = (
            db.query(func.count(LearningWeek.week_id))
            .filter(LearningWeek.status == "completed")
            .scalar()
            or 0
        )

        progress_percentage = (completed_count / total_weeks) * 100

        return NavigationResponse(
            current_week=LearningWeekResponse.from_orm(current_week),
            previous_week=LearningWeekResponse.from_orm(previous_week) if previous_week else None,
            next_week=LearningWeekResponse.from_orm(next_week) if next_week else None,
            total_weeks=total_weeks,
            progress_percentage=progress_percentage,
        )

    def get_curriculum_overview(self, db: Session) -> CurriculumOverviewResponse:
        """
        Get overview of entire curriculum with all weeks

        Args:
            db: Database session

        Returns:
            CurriculumOverviewResponse
        """
        weeks = db.query(LearningWeek).order_by(LearningWeek.week_number).all()

        # Count weeks by status
        completed = sum(1 for w in weeks if w.status == "completed")
        in_progress = sum(1 for w in weeks if w.status == "in_progress")
        not_started = sum(1 for w in weeks if w.status == "not_started")

        total_weeks = len(weeks)
        overall_progress = (completed / total_weeks * 100) if total_weeks > 0 else 0

        return CurriculumOverviewResponse(
            weeks=[LearningWeekResponse.from_orm(w) for w in weeks],
            total_weeks=total_weeks,
            completed_weeks=completed,
            in_progress_weeks=in_progress,
            not_started_weeks=not_started,
            overall_progress=overall_progress,
        )

    def update_week_status(self, db: Session, week_number: int, status: str) -> LearningWeek | None:
        """
        Update the status of a learning week

        Args:
            db: Database session
            week_number: Week number to update
            status: New status ('not_started', 'in_progress', 'completed')

        Returns:
            Updated LearningWeek or None
        """
        week = self.get_week_by_number(db, week_number)
        if not week:
            return None

        week.status = status
        db.commit()
        db.refresh(week)
        return week
