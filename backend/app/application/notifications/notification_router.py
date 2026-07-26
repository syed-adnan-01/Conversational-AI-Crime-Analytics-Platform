from fastapi import APIRouter, HTTPException, status
from typing import List
from .notification_models import (
    NotificationResponse, 
    NotificationCountResponse, 
    NotificationHealthResponse,
    NotificationCreate
)
from .notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])
service = NotificationService()

@router.get("", response_model=List[NotificationResponse])
def get_notifications():
    """Get all notifications."""
    return service.get_notifications()

@router.get("/unread", response_model=List[NotificationResponse])
def get_unread_notifications():
    """Get only unread notifications."""
    return service.get_notifications(unread_only=True)

@router.post("/read/{id}", status_code=status.HTTP_200_OK)
def mark_read(id: str):
    """Mark a notification as read."""
    success = service.mark_read(id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}

@router.post("/read-all", status_code=status.HTTP_200_OK)
def mark_all_read():
    """Mark all notifications as read."""
    count = service.mark_all_read()
    return {"message": f"{count} notifications marked as read"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(id: str):
    """Delete a notification."""
    success = service.delete_notification(id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")

@router.get("/count", response_model=NotificationCountResponse)
def get_notification_count():
    """Get total and unread notification counts."""
    return service.get_count()

@router.get("/health", response_model=NotificationHealthResponse)
def get_notification_health():
    """Get notification engine health status."""
    return service.get_health()

# Internal API for creating notifications (e.g. from AI/Investigation services)
@router.post("/internal/create", response_model=NotificationResponse)
def create_notification(data: NotificationCreate):
    return service.create_notification(data)
