"""
Endpoints pour la gestion des vidéos - Upload et statut.
"""
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.video_model import VideoUploadResponse, VideoStatus, ErrorResponse
from app.services.file_storage import FileStorageService

# Création du router pour les endpoints vidéo
router = APIRouter(prefix="/videos", tags=["videos"])


@router.post(
    "/upload",
    response_model=VideoUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload d'une vidéo",
    description="Permet d'uploader une vidéo qui sera stockée localement pour traitement ultérieur."
)
async def upload_video(file: UploadFile = File(..., description="Fichier vidéo à uploader")):
    """
    Endpoint pour uploader une vidéo.
    
    Args:
        file: Fichier vidéo uploadé
        
    Returns:
        VideoUploadResponse: Informations sur la vidéo uploadée
        
    Raises:
        HTTPException: En cas d'erreur lors de l'upload
    """
    try:
        # Génération d'un ID unique pour la vidéo
        video_id = str(uuid.uuid4())
        
        # Sauvegarde du fichier via le service de stockage
        unique_filename, full_path, file_size = await FileStorageService.save_video_file(file)
        
        # Création de la réponse
        response = VideoUploadResponse(
            video_id=video_id,
            filename=file.filename,
            file_path=full_path,
            file_size=file_size,
            content_type=file.content_type,
            status=VideoStatus.UPLOADED,
            message=f"Vidéo '{file.filename}' uploadée avec succès"
        )
        
        return response
        
    except HTTPException:
        # Re-lever les HTTPException du service de stockage
        raise
    except Exception as e:
        # Gestion des erreurs inattendues
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne lors de l'upload: {str(e)}"
        )


@router.get(
    "/health",
    summary="Vérification de l'état du service",
    description="Endpoint de santé pour vérifier que le service vidéo fonctionne correctement."
)
async def health_check():
    """
    Endpoint de vérification de l'état du service vidéo.
    
    Returns:
        Dict: Statut du service
    """
    return {
        "status": "healthy",
        "service": "video-upload",
        "message": "Service d'upload vidéo opérationnel"
    }


@router.get(
    "/stats",
    summary="Statistiques du stockage",
    description="Retourne des statistiques sur l'utilisation du stockage local."
)
async def get_storage_stats():
    """
    Endpoint pour obtenir des statistiques sur le stockage.
    
    Returns:
        Dict: Statistiques du stockage
    """
    try:
        from pathlib import Path
        from app.core.config import settings
        
        storage_path = Path(settings.local_video_path)
        
        if not storage_path.exists():
            return {
                "total_files": 0,
                "total_size_bytes": 0,
                "total_size_mb": 0,
                "storage_path": str(storage_path)
            }
        
        # Compter les fichiers et calculer la taille totale
        video_files = list(storage_path.glob("*"))
        total_files = len(video_files)
        total_size = sum(f.stat().st_size for f in video_files if f.is_file())
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "storage_path": str(storage_path)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des statistiques: {str(e)}"
        )
