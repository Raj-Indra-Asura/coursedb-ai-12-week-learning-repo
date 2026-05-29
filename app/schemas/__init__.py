"""
Pydantic Schemas for Request/Response Validation

Week 5-6: API Data Validation

Learning Objectives:
- Understand data validation with Pydantic
- Learn request/response schema separation
- Practice model design for APIs
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==========================================
# Enums for Validation
# ==========================================

class DifficultyEnum(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class ExamTypeEnum(str, Enum):
    midterm = "midterm"
    final = "final"
    quiz = "quiz"
    assignment = "assignment"


class ResourceTypeEnum(str, Enum):
    note = "note"
    textbook = "textbook"
    paper = "paper"
    video = "video"
    slide = "slide"


class SearchTypeEnum(str, Enum):
    sql = "sql"
    semantic = "semantic"
    hybrid = "hybrid"


class WeekStatusEnum(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class LearningResourceTypeEnum(str, Enum):
    documentation = "documentation"
    exercise = "exercise"
    solution = "solution"
    notebook = "notebook"
    code = "code"
    reflection = "reflection"


# ==========================================
# Course Schemas
# ==========================================

class CourseBase(BaseModel):
    course_code: str = Field(..., max_length=20, description="Unique course code (e.g., CS201)")
    course_title: str = Field(..., max_length=200, description="Full course title")
    semester: Optional[str] = Field(None, max_length=20, description="Semester offered")
    credit: int = Field(..., gt=0, description="Credit hours (must be > 0)")


class CourseCreate(CourseBase):
    """Request schema for creating a new course"""
    pass


class CourseUpdate(BaseModel):
    """Request schema for updating a course (all fields optional)"""
    course_code: Optional[str] = Field(None, max_length=20)
    course_title: Optional[str] = Field(None, max_length=200)
    semester: Optional[str] = Field(None, max_length=20)
    credit: Optional[int] = Field(None, gt=0)


class CourseResponse(CourseBase):
    """Response schema for course data"""
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode (SQLAlchemy)


# ==========================================
# Topic Schemas
# ==========================================

class TopicBase(BaseModel):
    course_id: int = Field(..., description="Foreign key to course")
    topic_name: str = Field(..., max_length=100, description="Topic/chapter name")
    description: Optional[str] = Field(None, description="Detailed description")
    week_number: int = Field(..., gt=0, description="Week number in course")


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    topic_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    week_number: Optional[int] = Field(None, gt=0)


class TopicResponse(TopicBase):
    topic_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Question Schemas
# ==========================================

class QuestionBase(BaseModel):
    course_id: int
    topic_id: Optional[int] = None
    question_text: str = Field(..., description="Full question text")
    course_code: Optional[str] = Field(None, max_length=20, description="Redundant for now (Week 4 fix)")
    topic_name: Optional[str] = Field(None, max_length=100, description="Redundant for now (Week 4 fix)")
    year: int = Field(..., ge=2010, le=2030, description="Year question was asked")
    exam_type: ExamTypeEnum
    difficulty: DifficultyEnum
    marks: int = Field(..., gt=0, description="Marks allocated")
    answer_text: Optional[str] = Field(None, description="Answer/solution")
    answer_reference: Optional[str] = Field(None, max_length=200, description="Reference for answer")


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    topic_id: Optional[int] = None
    year: Optional[int] = Field(None, ge=2010, le=2030)
    exam_type: Optional[ExamTypeEnum] = None
    difficulty: Optional[DifficultyEnum] = None
    marks: Optional[int] = Field(None, gt=0)
    answer_text: Optional[str] = None
    answer_reference: Optional[str] = None


class QuestionResponse(QuestionBase):
    question_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Resource Schemas
# ==========================================

class ResourceBase(BaseModel):
    course_id: int
    topic_id: Optional[int] = None
    title: str = Field(..., max_length=200)
    resource_type: ResourceTypeEnum
    file_path: Optional[str] = Field(None, max_length=500)
    url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    author: Optional[str] = Field(None, max_length=200)
    year_published: Optional[int] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    resource_type: Optional[ResourceTypeEnum] = None
    file_path: Optional[str] = Field(None, max_length=500)
    url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    author: Optional[str] = Field(None, max_length=200)
    year_published: Optional[int] = None


class ResourceResponse(ResourceBase):
    resource_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Search Schemas
# ==========================================

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    search_type: SearchTypeEnum = Field(SearchTypeEnum.sql, description="Type of search")
    top_k: int = Field(10, ge=1, le=100, description="Number of results to return")
    filters: Optional[dict] = Field(None, description="Additional filters (year, difficulty, topic_id)")


class SearchResult(BaseModel):
    question_id: Optional[int] = None
    resource_id: Optional[int] = None
    title: str
    snippet: str = Field(..., description="Text snippet showing match")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score (0-1)")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")


class SearchResponse(BaseModel):
    query: str
    search_type: SearchTypeEnum
    results: List[SearchResult]
    total_count: int
    execution_time_ms: float


# ==========================================
# Analytics Schemas
# ==========================================

class TopicFrequency(BaseModel):
    topic_name: str
    question_count: int
    avg_marks: float
    years: List[int]


class AnalyticsResponse(BaseModel):
    total_questions: int
    total_courses: int
    topics_by_frequency: List[TopicFrequency]
    questions_by_year: dict  # {year: count}
    questions_by_difficulty: dict  # {difficulty: count}


# ==========================================
# User Schemas (Week 11)
# ==========================================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=200)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Generic Responses
# ==========================================

class HealthResponse(BaseModel):
    status: str
    database: str
    message: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None


class DeleteResponse(BaseModel):
    message: str
    deleted_id: int


# ==========================================
# Learning Navigation Schemas
# ==========================================

class LearningWeekBase(BaseModel):
    week_number: int = Field(..., ge=1, le=12, description="Week number (1-12)")
    title: str = Field(..., max_length=200, description="Week title")
    description: Optional[str] = Field(None, description="Week description")
    directory_path: str = Field(..., max_length=500, description="Path to week directory")
    status: WeekStatusEnum = Field(WeekStatusEnum.not_started, description="Week completion status")


class LearningWeekCreate(LearningWeekBase):
    pass


class LearningWeekUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    status: Optional[WeekStatusEnum] = None


class LearningResourceBase(BaseModel):
    title: str = Field(..., max_length=200, description="Resource title")
    file_path: str = Field(..., max_length=500, description="Path to resource file")
    resource_type: LearningResourceTypeEnum = Field(..., description="Type of learning resource")
    description: Optional[str] = Field(None, description="Resource description")
    order_index: int = Field(0, description="Order within week")


class LearningResourceCreate(LearningResourceBase):
    week_id: int = Field(..., description="Foreign key to learning week")


class LearningResourceResponse(LearningResourceBase):
    resource_id: int
    week_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LearningWeekResponse(LearningWeekBase):
    week_id: int
    created_at: datetime
    updated_at: datetime
    resources: List[LearningResourceResponse] = Field(default_factory=list, description="Resources in this week")

    class Config:
        from_attributes = True


class NavigationResponse(BaseModel):
    current_week: LearningWeekResponse
    previous_week: Optional[LearningWeekResponse] = None
    next_week: Optional[LearningWeekResponse] = None
    total_weeks: int = 12
    progress_percentage: float = Field(..., ge=0, le=100, description="Overall curriculum progress")


class CurriculumOverviewResponse(BaseModel):
    weeks: List[LearningWeekResponse]
    total_weeks: int
    completed_weeks: int
    in_progress_weeks: int
    not_started_weeks: int
    overall_progress: float = Field(..., ge=0, le=100)


"""
Learning Notes:

Pydantic Features Demonstrated:
1. **Field Validation**: max_length, gt (greater than), ge (>=), le (<=)
2. **Optional Fields**: Optional[str] for nullable fields
3. **Enums**: Type-safe string choices (DifficultyEnum, ExamTypeEnum)
4. **Nested Models**: Lists and dicts for complex structures
5. **EmailStr**: Built-in email validation
6. **Config.from_attributes**: Enable SQLAlchemy ORM compatibility
7. **Separate Schemas**: Create vs Update vs Response (different validation rules)

Why Separate Schemas?
- **Create**: All required fields, no ID
- **Update**: All optional (partial updates)
- **Response**: Includes ID, timestamps, read-only fields

Example Usage in FastAPI:
```python
@router.post("/questions", response_model=QuestionResponse)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    # Pydantic validates input automatically
    # Return SQLAlchemy model → Pydantic converts to JSON
    pass
```

Next Steps:
- Implement CRUD operations in API endpoints
- Add error handling with ErrorResponse
- Test validation with invalid data
"""
