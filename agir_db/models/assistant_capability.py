from datetime import datetime
import uuid
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Float, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from agir_db.db.base_class import Base


class AssistantCapability(Base):
    """Assistant capability with integrated skill information and reinforcement learning metrics"""
    __tablename__ = "assistant_capabilities"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    assistant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assistants.id"), nullable=False, index=True)
    
    # Capability details (previously in separate table)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Proficiency metrics
    proficiency_level: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)  # Scale 1-5 (can be decimal now)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)  # 0-1 confidence in the proficiency level
    years_experience: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Reinforcement learning metrics
    success_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    feedback_sum: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # Sum of all feedback scores
    feedback_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # Count of feedback instances
    last_feedback_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Task history - can store task IDs and outcomes
    task_history: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    assistant: Mapped["Assistant"] = relationship("Assistant", foreign_keys=[assistant_id], back_populates="capabilities")
    
    # Method to recalculate proficiency based on feedback
    def update_proficiency_from_feedback(self, feedback_score: float, task_id: uuid.UUID = None):
        """
        Update proficiency level based on feedback using reinforcement learning principles
        
        Args:
            feedback_score: Float between 0-1 representing task performance
            task_id: UUID of the related task
        """
        # Record the feedback
        self.feedback_sum += feedback_score
        self.feedback_count += 1
        self.last_feedback_at = datetime.utcnow()
        
        # Update task history
        if task_id:
            if not self.task_history:
                self.task_history = {}
                
            self.task_history[str(task_id)] = {
                "feedback": feedback_score,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Increment success/failure counters
        if feedback_score >= 0.7:  # Good performance
            self.success_count += 1
        elif feedback_score <= 0.3:  # Poor performance
            self.failure_count += 1
            
        # Simple reinforcement learning update formula
        # Weighted average of current proficiency and new feedback
        # The weight of new feedback depends on confidence
        learning_rate = max(0.1, 1.0 - self.confidence_score)  # Lower confidence = higher learning rate
        
        # Convert feedback (0-1) to proficiency scale (1-5)
        feedback_as_proficiency = 1.0 + (feedback_score * 4.0)
        
        # Update proficiency using weighted average
        self.proficiency_level = (
            (1 - learning_rate) * self.proficiency_level + 
            learning_rate * feedback_as_proficiency
        )
        
        # Update confidence score
        # Increase confidence with more feedback
        consistency = 0.0
        if self.feedback_count > 1:
            avg_feedback = self.feedback_sum / self.feedback_count
            consistency = 1.0 - min(1.0, abs(feedback_score - avg_feedback) * 2)
            
        feedback_volume_factor = min(1.0, self.feedback_count / 10.0)  # Maxes out at 10 feedback points
        self.confidence_score = 0.3 * feedback_volume_factor + 0.7 * consistency 