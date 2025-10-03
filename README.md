# Apka Scheme (आपका स्कीम) 🇮🇳

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Your personal AI assistant for navigating Indian government schemes.**

Apka Scheme is an intelligent system that automatically scrapes, processes, and understands information from various state government portals to help you find relevant public welfare schemes through a simple chat interface.

---

## 🎯 The Problem

Government schemes are a cornerstone of public welfare in India, yet discovering them can be a significant challenge. Information is often scattered across numerous complex websites, buried in PDFs and circulars, and written in dense legal language. For a citizen, finding out which schemes they are eligible for can be a confusing and overwhelming process.

## ✨ The Solution

**Apka Scheme** tackles this challenge head-on. It acts as a smart aggregator and a helpful guide. The system works in a multi-stage pipeline:

1.  **Discovery & Scraping:** It starts with a list of state government portals and intelligently crawls them to find pages and documents related to schemes (`yojanas`).
2.  **Content Extraction:** It extracts clean, readable text from messy HTML pages and complex PDF documents.
3.  **Knowledge Base Creation:** All the extracted information is compiled into state-wise "wiki" pages, forming a centralized knowledge base.
4.  **AI-Powered Search:** Using state-of-the-art AI models, this knowledge base is converted into a vector database, enabling powerful semantic search.
5.  **Conversational AI:** A Retrieval-Augmented Generation (RAG) chatbot allows you to ask questions in plain English (e.g., *"I am a farmer in Maharashtra, what schemes are there for me?"*), and it provides accurate answers based on the scraped data, complete with sources.

## 🚀 Key Features

*   **Automated Multi-State Scraper:** A robust crawler designed to navigate government websites and identify relevant content.
*   **HTML & PDF Content Extraction:** Capable of parsing both web pages and official PDF documents to extract vital information.
*   **AI-Powered Semantic Search:** Utilizes a Retrieval-Augmented Generation (RAG) pipeline to find the most relevant information, not just keyword matches.
*   **Natural Language Chatbot:** An intuitive interface (powered by Google's Gemini) to ask questions and get clear, summarized answers.
*   **Source-Grounded Responses:** Every answer provided by the chatbot is backed by links to the original government source documents.
*   **Change Detection:** A versioning system to track when scheme information on a government portal has been updated.

## 🔧 Tech Stack & Architecture

*   **Data Collection:** `Requests`, `BeautifulSoup4`
*   **PDF Processing:** `pdfplumber`
*   **NLP & AI Core:**
    *   Text Processing: `NLTK`
    *   Embeddings: `sentence-transformers` (all-MiniLM-L6-v2)
    *   Vector Index: `scikit-learn` (`NearestNeighbors`)
    *   Generative Model: `google-generativeai` (Gemini Pro)
*   **Data Storage:** `Pickle` (for vector store), `SQLite` (for versioning)
*   **Web Interface (Demo):** `Flask`, `ngrok`

## 📁 Project Structure

```
.
├── state_wikis/            # Auto-generated Markdown knowledge bases for each state
├── my_embedding_model/     # Saved Sentence Transformer model
├── pdfs/                   # Downloaded PDF documents
├── raw_html/               # Raw HTML files from the scrape
├── all_extracted_content.json # All scraped text in a single file
├── vector_store.pkl        # The saved vector database (embeddings + metadata)
├── nn_index.pkl            # The saved search index
├── Gov_Web_Scrapper_Bot.ipynb # The main Jupyter Notebook for the pipeline
└── README.md
```

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/apka-scheme.git
    cd apka-scheme
    ```

2.  **Install dependencies:**
    (It is highly recommended to use a virtual environment)
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Create a `requirements.txt` file by running `pip freeze > requirements.txt` in your Colab environment after all installs are complete.)*

3.  **Set up API Key:**
    *   Get a free API key from [Google AI Studio](https://aistudio.google.com/).
    *   Create a `.env` file in the root directory and add your key:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```
    *   The chatbot code will automatically load this key.

## ▶️ How to Run the Pipeline

The project is structured as a Jupyter Notebook (`Gov_Web_Scrapper_Bot.ipynb`). To generate the knowledge base and run the chatbot, execute the cells in the following order:

1.  **Setup Cells (1-4):** Run these to install libraries, define helper functions, and set the seed URLs.
2.  **Main Crawling & Extraction Cell:** Run the consolidated block that crawls all state websites and generates `all_extracted_content.json`.
3.  **Wiki Generation Cell:** Run this to process the JSON file and create the Markdown files in the `state_wikis/` directory.
4.  **Vector Database Cell:** Run this to load the AI model, chunk the documents, create embeddings, and save the `vector_store.pkl` and `nn_index.pkl` files.
5.  **Chatbot Cell:** Run the final cell to start interacting with the RAG chatbot and ask your questions!

## 💡 Future Improvements

-   [ ] **Transition to a Production Vector Database:** Replace the `pickle` + `scikit-learn` index with a more robust solution like FAISS, ChromaDB, or a managed service.
-   [ ] **Improve the Scraper:** Integrate tools like Selenium or Playwright to handle JavaScript-heavy websites that the current `requests`-based scraper misses.
-   [ ] **Develop a User-Friendly UI:** Replace the demo Flask app with a proper frontend framework (like Streamlit or React) for a better user experience.
-   [ ] **Add More States:** Expand the `seeds.csv` list to cover all states and union territories in India.
-   [ ] **Fine-tune the RAG Prompt:** Continuously refine the prompt sent to the LLM to improve the quality and formatting of the answers.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
