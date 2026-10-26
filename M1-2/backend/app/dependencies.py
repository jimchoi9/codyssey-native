"""Lazy external boundaries; tests override providers without loading credentials."""
from functools import lru_cache
from uuid import uuid4

from .config import get_settings
from .ports import ChatGateway, ConversationRepository, DataRepository, GenerationUnavailable, StorageUnavailable


@lru_cache(maxsize=4)
def _build_firestore_client(project_id: str, credential_path: str):
    from firebase_admin import credentials, firestore, initialize_app
    certificate = credentials.Certificate(credential_path)
    firebase_app = initialize_app(certificate, {"projectId": project_id}, name=f"story-analytics-{uuid4().hex}")
    return firestore.client(app=firebase_app)


def get_data_repository() -> DataRepository:
    settings = get_settings()
    if not settings.firebase_project_id or not settings.google_application_credentials:
        raise StorageUnavailable("Data storage is not configured")
    try:
        from .data.repository import FirestoreDataRepository
        client = _build_firestore_client(settings.firebase_project_id, settings.google_application_credentials)
        return FirestoreDataRepository(client)
    except Exception:
        raise StorageUnavailable("Storage is temporarily unavailable.") from None


def get_conversation_repository() -> ConversationRepository:
    raise StorageUnavailable("Conversation storage is not configured")


def get_chat_gateway() -> ChatGateway:
    raise GenerationUnavailable("Answer generation is not configured")
