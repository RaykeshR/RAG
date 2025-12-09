from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangchainDocument
import os

class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def load_and_chunk_file(self, file_path: str):
        """
        Loads a single file and splits it into chunks using Langchain.
        Automatically detects loader based on file extension.
        """
        _, file_extension = os.path.splitext(file_path)
        loader = None
        if file_extension.lower() == ".txt":
            loader = TextLoader(file_path)
        elif file_extension.lower() == ".pdf":
            loader = PyPDFLoader(file_path)
        # Add more loaders for other file types as needed
        # elif file_extension.lower() == ".docx":
        #     loader = Docx2txtLoader(file_path)
        
        if loader:
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            return chunks
        else:
            print(f"No suitable loader found for file: {file_path}")
            return []

    def load_and_chunk_directory(self, directory_path: str):
        """
        Loads all supported files from a directory and splits them into chunks.
        """
        if not os.path.isdir(directory_path):
            print(f"Directory not found: {directory_path}")
            return []

        # This will load all supported file types by Langchain's DirectoryLoader
        # For more control, one can specify glob patterns or use specific loaders
        # Example for specific loaders:
        # loader = DirectoryLoader(directory_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
        
        # Using a more generic approach to find files and load them individually
        all_chunks = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Filter for supported types
                if file.lower().endswith(('.txt', '.pdf')): # Extend as more loaders are added
                    print(f"Loading and chunking file: {file_path}")
                    chunks = self.load_and_chunk_file(file_path)
                    all_chunks.extend(chunks)
                else:
                    print(f"Skipping unsupported file type: {file_path}")
        return all_chunks

if __name__ == "__main__":
    # Example usage:
    processor = DocumentProcessor()

    # Create a dummy directory and files for testing
    if not os.path.exists("../test_data"):
        os.makedirs("../test_data")
    with open("../test_data/sample.txt", "w") as f:
        f.write("This is a sample text document. It has some content.")
    # For PDF, you would need an actual PDF file.
    # For now, we'll just test with text.

    print("--- Loading from directory ---")
    chunks_from_dir = processor.load_and_chunk_directory("../test_data")
    print(f"Loaded {len(chunks_from_dir)} chunks from directory.")
    for i, chunk in enumerate(chunks_from_dir):
        print(f"Chunk {i+1}: {chunk.page_content[:50]}... (Source: {chunk.metadata.get('source')})")

    # Clean up test data
    os.remove("../test_data/sample.txt")
    os.rmdir("../test_data")