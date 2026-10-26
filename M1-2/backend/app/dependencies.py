"""Override these providers in tests; external adapters arrive in later stages."""
from .ports import ChatGateway, ConversationRepository, DataRepository, GenerationUnavailable, StorageUnavailable


def get_data_repository() -> DataRepository:
    raise StorageUnavailable('Data storage is not configured')


def get_conversation_repository() -> ConversationRepository:
    raise StorageUnavailable('Conversation storage is not configured')


def get_chat_gateway() -> ChatGateway:
    raise GenerationUnavailable('Answer generation is not configured')
