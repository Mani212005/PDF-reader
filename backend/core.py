import os
import asyncio
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains.summarize import load_summarize_chain

async def create_qa_chain_async(api_key: str, pdf_path: str):
    """
    Creates a RetrievalQA chain for a given PDF file.

    Args:
        api_key (str): The Google API key.
        pdf_path (str): The path to the PDF file.

    Returns:
        RetrievalQA: The RetrievalQA chain.
    """
    # Load document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Create vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = await Chroma.from_documents(texts, embeddings)

    # Create QA chain
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.3)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
    )
    return qa_chain

def create_qa_chain(api_key: str, pdf_path: str):
    return asyncio.run(create_qa_chain_async(api_key, pdf_path))

async def summarize_pdf_async(api_key: str, pdf_path: str):
    """
    Summarizes the content of a given PDF file.

    Args:
        api_key (str): The Google API key.
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The summary of the PDF.
    """
    # Load document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # The 'map_reduce' chain type is effective for summarizing large documents.
    # It first summarizes smaller chunks (map step) and then combines those summaries
    # into a final summary (reduce step).
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0)
    summary_chain = load_summarize_chain(llm=llm, chain_type="map_reduce")
    
    summary = await summary_chain.arun(documents)
    return summary

def summarize_pdf(api_key: str, pdf_path: str):
    return asyncio.run(summarize_pdf_async(api_key, pdf_path))