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
            """Answer the question based only on the following context:
            {context}

            Question: {question}
            """
        )
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.output_parser

    def generate_response(self, query: str, documents: list):
        """
        Generates a response based on the query and retrieved/reranked documents using an LLM.
        """
        if not documents:
            return "I couldn't find any relevant information in the knowledge base for your query."

        context = "\n\n".join([doc["content"] for doc in documents])
        
        try:
            response = self.chain.invoke({"context": context, "question": query})
            return response
        except Exception as e:
            return f"An error occurred while generating response: {str(e)}"