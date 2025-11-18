# 🚀 ResumeRAG Setup Guide

Complete installation and setup guide for the ResumeRAG AI-Powered Career Intelligence Platform.

## 📋 Prerequisites

- Python 3.10+
- pip (Python package manager)
- Git
- 4GB+ RAM
- 2GB+ free disk space

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MEKALA-JASWANTH/ResumeRAG.git
cd ResumeRAG
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\\Scripts\\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

### Option 1: Run Backend API

```bash
cd backend
python main.py
```

API will be available at:
- **Main**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Option 2: Using uvicorn

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### 1. Upload Documents

```bash
curl -X POST http://localhost:8000/upload \\
  -F "files=@your_document.pdf"
```

### 2. Query Documents

```bash
curl -X POST http://localhost:8000/query \\
  -H "Content-Type: application/json" \\
  -d '{"query":"What is machine learning?","k":5}'
```

### 3. Get Stats

```bash
curl http://localhost:8000/stats
```

### 4. Health Check

```bash
curl http://localhost:8000/health
```

## 🧪 Testing

### Test with Python

```python
import requests

# Upload document
with open('sample.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'files': f}
    )
    print(response.json())

# Query
response = requests.post(
    'http://localhost:8000/query',
    json={'query': 'Explain RAG', 'k': 3}
)
print(response.json())
```

## 📁 Project Structure

```
ResumeRAG/
├── backend/
│   ├── rag_engine/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── rag_pipeline.py
│   └── main.py
├── requirements.txt
├── README.md
├── SETUP.md
└── LICENSE
```

## 🔑 Configuration

### Environment Variables (Optional)

Create `.env` file:

```env
OPENAI_API_KEY=your_key_here
CHROMA_PERSIST_DIR=./chroma_db
UPLOAD_DIR=./uploads
```

## 🐛 Troubleshooting

### Issue: Module not found

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: ChromaDB errors

```bash
pip install chromadb --upgrade
```

### Issue: Port already in use

```bash
uvicorn main:app --port 8001
```

## 📚 Usage Examples

### 1. Index Study Materials

```python
from rag_engine.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
result = pipeline.index_documents([
    'ssc_cgl_2023.pdf',
    'polity_notes.pdf'
])
print(f"Indexed {result['chunks']} chunks")
```

### 2. Search Documents

```python
results = pipeline.search(
    "What topics were asked in SSC CGL?",
    k=5
)

for result in results['results']:
    print(result['content'])
    print(result['metadata'])
```

## 🚀 Production Deployment

### Using Gunicorn

```bash
cd backend
gunicorn main:app \\
  --workers 4 \\
  --worker-class uvicorn.workers.UvicornWorker \\
  --bind 0.0.0.0:8000
```

### Using Docker (Coming Soon)

```bash
docker-compose up -d
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 💬 Support

- 📧 Email: support@resumerag.com
- 🐛 Issues: [GitHub Issues](https://github.com/MEKALA-JASWANTH/ResumeRAG/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/MEKALA-JASWANTH/ResumeRAG/discussions)

## 🙏 Acknowledgments

- LangChain for RAG framework
- ChromaDB for vector storage
- Sentence Transformers for embeddings
- FastAPI for web framework

---

**Built with ❤️ for students preparing for competitive exams and software jobs**
