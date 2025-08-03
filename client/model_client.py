from transformers import AutoTokenizer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model

from core.settings import settings


model_name = settings.HF_EMBEDDING_MODEL
embedding_model = HuggingFaceEmbeddings(model_name=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

llm = init_chat_model(settings.CHAT_MODEL, model_provider=settings.MODEL_PROVIDER, **{"temperature": settings.TEMPERATURE})