"""
Connecteur MongoDB pour la gestion des métadonnées vidéo.
Module préparé pour l'intégration future avec MongoDB.
"""
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from app.core.config import settings
from app.models.video_model import VideoMetadata


class MongoDBConnector:
    """
    Gestionnaire de connexion MongoDB pour les métadonnées vidéo.
    
    Note: Ce module est préparé pour l'intégration future avec MongoDB.
    Pour l'instant, il n'est pas utilisé dans le workflow principal.
    """
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
        self.collection = None
    
    async def connect(self) -> bool:
        """
        Établit la connexion à MongoDB.
        
        Returns:
            bool: True si la connexion est réussie, False sinon
        """
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_url)
            # Test de la connexion
            await self.client.admin.command('ping')
            self.database = self.client[settings.mongodb_database]
            self.collection = self.database.video_metadata
            return True
        except ConnectionFailure:
            return False
    
    async def disconnect(self):
        """Ferme la connexion à MongoDB."""
        if self.client:
            self.client.close()
    
    async def save_video_metadata(self, metadata: VideoMetadata) -> bool:
        """
        Sauvegarde les métadonnées d'une vidéo.
        
        Args:
            metadata: Métadonnées de la vidéo
            
        Returns:
            bool: True si la sauvegarde est réussie
        """
        try:
            if self.collection is None:
                return False
            
            # Convertir en dict et gérer les dates
            metadata_dict = metadata.model_dump()
            await self.collection.insert_one(metadata_dict)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des métadonnées: {e}")
            return False
    
    async def get_video_metadata(self, video_id: str) -> Optional[VideoMetadata]:
        """
        Récupère les métadonnées d'une vidéo par son ID.
        
        Args:
            video_id: Identifiant de la vidéo
            
        Returns:
            VideoMetadata ou None si non trouvé
        """
        try:
            if self.collection is None:
                return None
            
            doc = await self.collection.find_one({"video_id": video_id})
            if doc:
                # Supprimer le champ _id de MongoDB pour éviter les problèmes de sérialisation
                doc.pop('_id', None)
                return VideoMetadata(**doc)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération des métadonnées: {e}")
            return None
    
    async def update_video_status(self, video_id: str, new_status: str) -> bool:
        """
        Met à jour le statut d'une vidéo.
        
        Args:
            video_id: Identifiant de la vidéo
            new_status: Nouveau statut
            
        Returns:
            bool: True si la mise à jour est réussie
        """
        try:
            if self.collection is None:
                return False
            
            result = await self.collection.update_one(
                {"video_id": video_id},
                {"$set": {"status": new_status}}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    async def list_all_videos(self) -> List[VideoMetadata]:
        """
        Liste toutes les vidéos en base.
        
        Returns:
            List[VideoMetadata]: Liste des métadonnées
        """
        try:
            if self.collection is None:
                return []
            
            cursor = self.collection.find({}).sort("upload_time", -1)  # Tri par date décroissante
            videos = []
            async for doc in cursor:
                # Supprimer le champ _id de MongoDB
                doc.pop('_id', None)
                videos.append(VideoMetadata(**doc))
            return videos
        except Exception as e:
            print(f"Erreur lors de la liste des vidéos: {e}")
            return []


# Instance globale du connecteur (à utiliser quand MongoDB sera configuré)
mongodb_connector = MongoDBConnector()
