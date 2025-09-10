# PDF QA & Summarization Assistant

This is a web-based application that allows you to chat with your PDF documents and get summaries of them. You can ask questions about the content of a PDF file, and the application will use a large language model to provide answers.

## Features

*   **Question Answering:** Ask questions about your PDF documents in natural language.
*   **Summarization:** Get a concise summary of your PDF documents.
*   **Secure API Key Handling:** Your API key is stored locally in a `.env` file and is not exposed in the user interface.
*   **Powered by Google Gemini:** Uses the Google Gemini Pro model for question answering and summarization.

## Technologies Used

*   **Streamlit:** For the web interface.
*   **LangChain:** For building the question-answering and summarization chains.
*   **Google Generative AI:** For the large language model.
*   **ChromaDB:** For creating a vector store of the PDF content.
*   **PyPDF2:** For reading and extracting text from PDF files.

## Setup and Usage

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Mani212005/PDF-reader.git
    cd PDF-reader
    ```

2.  **Create a virtual environment and install the dependencies:**

    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**

    Create a file named `.env` in the root of the project and add your Google API key to it:

    ```
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
    ```

4.  **Run the application:**

    ```bash
    streamlit run streamlit/front.py
    ```

## Configuration

The application requires a Google API key to function. You can get a free API key from the [Google AI Studio](https://aistudio.google.com/).
