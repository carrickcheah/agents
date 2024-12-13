from langchain_community.document_loaders import S3DirectoryLoader
from langchain_openai import OpenAIEmbeddings




def main(
        aws_access_key_id: str,
        aws_secret_access_key: str,
        openai_api_key: str,
        qdrant_host: str
       
):
    print("Hello from rag!")


# Initialize the S3 document loader
    loader = S3DirectoryLoader(
    "product-dataset",  # S3 bucket name
    "p_1", #S3 Folder name containing the data for the first product
    aws_access_key_id=aws_access_key_id,  # AWS Access Key
    aws_secret_access_key=aws_secret_access_key  # AWS Secret Access Key
    )

    # Load documents from the specified S3 bucket
    docs = loader.load()

    # Initialize the text embedding model from OpenAI
    text_embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")










if __name__ == "__main__":
    from config import config
    main(
        aws_secret_access_key=config.aws_secret_access_key,
        aws_secret_access_key=config.aws_secret_access_key,
        openai_api_key=config.openai_api_key,
        qdrant_key=config.qdrant_key

    )
