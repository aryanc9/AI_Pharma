from langfuse import Langfuse
import os


langfuse = Langfuse(
    public_key=os.getenv("pk-lf-d3bc78ff-6f68-4104-8596-e4e423b6c106"),
    secret_key=os.getenv("sk-lf-75812084-bd8d-4b65-b11a-1c72876138c9"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

