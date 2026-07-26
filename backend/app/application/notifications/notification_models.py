from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class NotificationCategory(str, Enum):
    SYSTEM = "SYSTEM"
    CASE = "CASE"
    INVESTIGATION = "INVESTIGATION"
    EVIDENCE = "EVIDENCE"
    AI = "AI"
    LEGAL = "LEGAL"
    ADMIN = "ADMIN"

class NotificationPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class NotificationBase(BaseModel):
    title: str = Field(..., description="The title of the notification")
    message: str = Field(..., description="The main message content")
    category: NotificationCategory = Field(..., description="The category of the notification")
    priority: NotificationPriority = Field(..., description="The priority level of the notification")
    source: str = Field(..., description="The source that generated this notification")

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    notification_id: str = Field(..., description="Unique identifier for the notification")
    created_at: datetime = Field(..., description="When the notification was created")
    read: bool = Field(False, description="Whether the notification has been read")

class NotificationCountResponse(BaseModel):
    total: int
    unread: int

class NotificationHealthResponse(BaseModel):
    status: str
    storage_status: str
    total_notifications: int
