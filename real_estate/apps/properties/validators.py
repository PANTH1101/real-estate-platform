import os
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_image_file(value):
    """Validate uploaded image file extension and size."""
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Check file size (10MB max)
    if value.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError("File size exceeds 10MB limit.")


def validate_video_file(value):
    """Validate uploaded video file extension and size."""
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
        raise ValidationError(
            f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_VIDEO_EXTENSIONS)}"
        )
    
    # Check file size (50MB max for videos)
    max_video_size = 50 * 1024 * 1024
    if value.size > max_video_size:
        raise ValidationError("Video file size exceeds 50MB limit.")

