from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

class Generator:
    def __init__(self, llm_model_name="mistral"):
        # Initialize a Langchain LLM using Ollama.
        # This can be replaced with any Ollama-compatible model.
        # Ensure you have Ollama running locally with the specified model pulled (e.g., `ollama pull mistral`).
        self.llm = ChatOllama(model=llm_model_name, temperature=0.0)

        # Define a prompt template for RAG
        self.prompt = ChatPromptTemplate.from_template(
            """Answer the question based only on the following context. For each piece of information you use, you must cite the source.

            Context:
            {context}

            Question: {question}

            Answer:
            """
        )
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.output_parser

    def generate_response(self, query: str, documents: list):
        """
        Generates a response based on the query and retrieved/reranked documents using an LLM.
        If any document lacks a source, returns a message listing the top-k documents.
        """
        if not documents:
            return "I couldn't find any relevant information in the knowledge base for your query."

        # Check if all documents have a source
        all_docs_have_source = True
        for doc in documents:
            # Check if 'source' key exists and its value is not empty or None
            if not doc['metadata'].get('source'):
                all_docs_have_source = False
                break
        
        if not all_docs_have_source:
            # If any document lacks a source, return the raw documents
            formatted_docs = []
            for i, doc in enumerate(documents):
                source_info = doc['metadata'].get('source', 'Source not available')
                formatted_docs.append(f"Document {i+1} (Source: {source_info}):\nContent: {doc['content']}\n")
            return "Some sources were not found for the retrieved documents. Here are the top documents:\n\n" + "\n".join(formatted_docs)

        # If all documents have sources, proceed with LLM generation
        context = ""
        for doc in documents:
            context += f"Source: {doc['metadata'].get('source', 'N/A')}\n"
            context += f"Content: {doc['content']}\n\n"
        
        try:
            response = self.chain.invoke({"context": context, "question": query})
            return response
        except Exception as e:
            return f"An error occurred while generating response: {str(e)}"