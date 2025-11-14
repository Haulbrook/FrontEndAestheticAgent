"""
Data models for the Disney Trip Planning Agent
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ChecklistItem(BaseModel):
    """Represents a single checklist item"""
    id: str
    text: str
    completed: bool = False
    category: str = "general"
    priority: str = "medium"  # low, medium, high
    deadline: Optional[str] = None


class TripDetails(BaseModel):
    """Represents trip information"""
    destination: str = "Walt Disney World"
    start_date: datetime
    end_date: datetime
    party_size: int = 1
    ages: List[int] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    budget_range: Optional[str] = None
    special_needs: List[str] = Field(default_factory=list)


class IdeaSuggestion(BaseModel):
    """Represents a brainstormed idea or suggestion"""
    id: str
    title: str
    description: str
    category: str
    tags: List[str] = Field(default_factory=list)
    saved: bool = False


class TripPlan(BaseModel):
    """Complete trip plan"""
    trip_details: TripDetails
    checklists: List[ChecklistItem] = Field(default_factory=list)
    ideas: List[IdeaSuggestion] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
