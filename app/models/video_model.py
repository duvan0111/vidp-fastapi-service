"""
Modèles Pydantic pour les données vidéo.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class VideoStatus(str, Enum):
    """Statuts possibles pour une vidéo."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoUploadResponse(BaseModel):
    """Réponse après l'upload d'une vidéo."""
    video_id: str = Field(..., description="Identifiant unique de la vidéo")
    filename: str = Field(..., description="Nom original du fichier")
    file_path: str = Field(..., description="Chemin local du fichier sauvegardé")
    file_size: int = Field(..., description="Taille du fichier en octets")
    content_type: str = Field(..., description="Type MIME du fichier")
    status: VideoStatus = Field(default=VideoStatus.UPLOADED, description="Statut de la vidéo")
    upload_time: datetime = Field(default_factory=datetime.now, description="Horodatage de l'upload")
    message: str = Field(default="Vidéo uploadée avec succès", description="Message de statut")


class VideoMetadata(BaseModel):
    """Métadonnées d'une vidéo (pour usage futur avec MongoDB)."""
    video_id: str
    original_filename: str
    file_path: str
    file_size: int
    content_type: str
    status: VideoStatus
    upload_time: datetime
    processing_start_time: Optional[datetime] = None
    processing_end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class VideoStatusResponse(BaseModel):
    """Réponse pour le statut d'une vidéo."""
    video_id: str
    status: VideoStatus
    message: str
    upload_time: Optional[datetime] = None
    processing_progress: Optional[float] = Field(None, ge=0.0, le=1.0, description="Progression du traitement (0-1)")


class ErrorResponse(BaseModel):
    """Réponse d'erreur standardisée."""
    error: str
    detail: str
    timestamp: datetime = Field(default_factory=datetime.now)
