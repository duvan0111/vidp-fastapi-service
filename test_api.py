#!/usr/bin/env python3
"""
Script de test pour l'API d'upload vidéo VidP.
"""
import requests
import json
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{API_BASE_URL}/api/v1/videos/upload"

def create_test_video_file():
    """Crée un fichier vidéo de test (simulé avec du texte)."""
    test_file_path = Path("test_video.mp4")
    
    # Créer un fichier de test avec du contenu binaire simulé
    test_content = b"FAKE VIDEO CONTENT - This is a test file for video upload simulation"
    
    with open(test_file_path, "wb") as f:
        f.write(test_content)
    
    return test_file_path

def test_video_upload():
    """Teste l'upload d'une vidéo via l'API."""
    print("🎬 Test d'upload vidéo VidP")
    print("=" * 50)
    
    # Créer un fichier de test
    test_file = create_test_video_file()
    print(f"📁 Fichier de test créé: {test_file}")
    
    try:
        # Préparer le fichier pour l'upload
        with open(test_file, "rb") as f:
            files = {
                'file': ('test_video.mp4', f, 'video/mp4')
            }
            
            print(f"📤 Upload vers: {UPLOAD_ENDPOINT}")
            
            # Faire la requête d'upload
            response = requests.post(UPLOAD_ENDPOINT, files=files)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Upload réussi!")
                print(f"🆔 Video ID: {result['video_id']}")
                print(f"📄 Filename: {result['filename']}")
                print(f"📍 File Path: {result['file_path']}")
                print(f"📏 File Size: {result['file_size']} bytes")
                print(f"🏷️  Content Type: {result['content_type']}")
                print(f"⏰ Upload Time: {result['upload_time']}")
                print(f"💬 Message: {result['message']}")
            else:
                print("❌ Erreur lors de l'upload")
                print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que le serveur FastAPI est en cours d'exécution")
    
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    finally:
        # Nettoyer le fichier de test
        if test_file.exists():
            test_file.unlink()
            print(f"🧹 Fichier de test supprimé: {test_file}")

def test_api_health():
    """Teste les endpoints de santé de l'API."""
    print("\n🏥 Test des endpoints de santé")
    print("=" * 50)
    
    endpoints = [
        ("API Root", f"{API_BASE_URL}/"),
        ("API Health", f"{API_BASE_URL}/health"),
        ("Video Health", f"{API_BASE_URL}/api/v1/videos/health"),
        ("Storage Stats", f"{API_BASE_URL}/api/v1/videos/stats"),
        ("Status Health", f"{API_BASE_URL}/api/v1/status/health")
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Erreur - {e}")

if __name__ == "__main__":
    print("🚀 Test de l'API VidP FastAPI Service")
    print("=" * 60)
    
    test_api_health()
    test_video_upload()
    
    print("\n" + "=" * 60)
    print("✨ Tests terminés!")
