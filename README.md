# Flowbit AI Internship Project

## Multi-Agent AI System for Document Processing

A system that classifies and processes PDF, JSON, and Email inputs using specialized AI agents.

## Features

- **Classifier Agent**: Detects document format and intent
- **Specialized Agents**:
  - PDF Agent (Invoice extraction)
  - JSON Agent (Schema validation)
  - Email Agent (Header parsing)
- **Shared Memory**: Tracks processing context
- **Modular Design**: Easy to extend with new agents

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flowbit-ai-internship.git
   cd flowbit-ai-internship

2.Set up virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
Install dependencies:

bash
pip install -r requirements.txt
Set up Ollama (for local LLM processing):

bash
ollama pull llama3
Usage
Basic Command
bash
python main.py --input samples/invoice.pdf
Sample Inputs
Place test files in the samples/ directory:

invoice.pdf - Sample invoice PDF

email.txt - Raw email text

data.json - JSON payload
