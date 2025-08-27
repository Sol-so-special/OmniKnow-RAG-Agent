import chromadb
import uuid
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

client = chromadb.Client()
web_data_collection = client.get_or_create_collection("web_data_collection")

# Initialize the Sentence Transformer model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_web_data(url):
    try:
        # Create a WebBaseLoader instance with the provided URL
        loader = WebBaseLoader(url)
        
        # Load the web page conten
        data = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        page_chunks = text_splitter.split_documents(data)
        
        print(f"Loaded {len(page_chunks)} chunks from {url}")
        return page_chunks

    except Exception as e:
        print(f"Error loading web data: {str(e)}")
        return None

def process_web_data(data):
    if data is None:
        print("No data to process.")
        return False
    
    # Prepare chunks, embeddings, metadata, and ids
    chunks, metadatas, ids = [], [], []

    for index, chunk in enumerate(data):
        # Extract chunk content
        chunks.append(chunk.page_content)

        # Prepare metadatas
        metadatas.append({
            'source_url': chunk.metadata.get('source', 'unknown'),
            'chunk_number': index + 1
        })
        
        ids.append(str(uuid.uuid4()))  # Generate unique IDs for each chunk

    # Embed the chunks
    embeddings = model.embed_documents(chunks)
    
    # Add chunks to the ChromaDB collection
    web_data_collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    num_of_chunks = len(chunks)
    print(f"Stored {num_of_chunks} chunk{'' if num_of_chunks < 2 else 's'} in ChromaDB.")
    return True

def add_web_data(url):
    # Load web data from the given URL
    print(f"Loading data from {url}...")
    web_data = load_web_data(url)

    # Process web data and add it to the ChromaDB collection
    if process_web_data(web_data):
        print("Web data processing complete.")