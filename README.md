# Valio Aimo Junction 2025 - Predictive Inventory & Substitute Recommendation Platform

## Overview

This repository contains a predictive inventory and substitute recommendation system for the Valio Aimo Junction 2025 hackathon. It leverages sales, replacement, purchase, and product data to forecast stock-outs, optimize buffer margins, and recommend substitutes using machine learning, vector search, LLMs, and workflow automation.

---

## Data Sources

- **Sales Orders:**  
  `valio_aimo_sales_and_deliveries_junction_2025.csv`  
  Sales order rows with delivery and picking info for 1 year. Each row may have multiple deliveries and transfer orders.

- **Replacement Orders:**  
  `valio_aimo_replacement_orders_junction_2025.csv`  
  Orders created to cover shortages. Product codes and customer numbers match sales data.

- **Purchase Orders:**  
  `valio_aimo_purchases_junction_2025.csv`  
  Purchase order rows and received quantities. Product codes match sales and replacement data.

- **Product Data:**  
  `valio_aimo_product_data_junction_2025.json`  
  Rich product metadata for semantic search and recommendations.

---

## Architecture
![/Users/untitled_folder/Abroad/Masters/EIT Digital Masters/ETE HU/Sem 3/Junction/architecture diagram/diagram-export-15-11-2025-11_14_01-PM.png]

- **PostgreSQL Database:**  
  Stores structured sales, replacement, purchase, and product data.
- **Feature Engineering & ML Model:**  
  Predicts buffer margin and confidence score for stock-outs.
- **Vector Database (Milvus/Zilliz):**  
  Stores product embeddings for semantic search and RAG.
- **LLM Integration (Claude/OpenAI):**  
  Generates substitute recommendations and automates communication.
- **Voice AI (ElevenLabs):**  
  Produces natural language voice responses for warehouse/customer interactions.
- **AR Devices (Snapchat Spectacles):**  
  Enables AR-guided picking and real-time quality verification.
- **Workflow Automation (n8n):**  
  Orchestrates business logic, integrations, and event-driven processes.
- **SAP Integration:**  
  Designed for production use with real-time data (not included in hackathon data).

---

## n8n Workflows

The `/n8n nodes/` folder contains JSON definitions for key workflows:
- **Stock-Out Prediction & Substitution**
- **Supplier Reliability & Buffer Optimization**
- **AR-Guided Picking & Quality Verification**
- **Customer Communication & Substitution Management**
- **Claims & Remediation Automation**

Import these into n8n and configure endpoints for LLM, ElevenLabs, SAP, etc.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Install Dependencies

- **Python:**  
  `pip install -r requirements.txt`
- **PostgreSQL:**  
  Install and start PostgreSQL (`brew install postgresql` on Mac).
- **Milvus/Zilliz:**  
  Follow [Milvus](https://milvus.io/docs/install_standalone-docker.md) or [Zilliz Cloud](https://zilliz.com/) setup guides.
- **n8n:**  
  Install n8n (`npm install n8n -g` or use Docker).
- **ElevenLabs API:**  
  Get API key and configure in n8n nodes.
- **LLM API (Claude/OpenAI):**  
  Get API key and configure in n8n nodes.
- **Snapchat Spectacles:**  
  Set up device and connect to n8n workflow for AR guidance.

### 3. Database Setup

- Create tables using `schema.sql`:
  ```bash
  psql -U <user> -d <dbname> -f schema.sql
  ```
- Load CSVs into tables:
  ```bash
  python scripts/load_csvs.py
  ```

### 4. Product Embedding & Vector DB

- Run the embedding script to process product data and upload to Milvus/Zilliz:
  ```bash
  python scripts/embed_products.py
  ```

### 5. Train ML Model

- Train the buffer margin prediction model:
  ```bash
  python scripts/train_model.py
  ```

### 6. Import n8n Workflows

- Import JSON files from `/n8n nodes/` into your n8n instance.
- Configure credentials and endpoints for ElevenLabs, LLM, and SAP (if available).

### 7. Run API Service

- Start the FastAPI service:
  ```bash
  uvicorn api.main:app --reload
  ```

---

## Usage

- **Predict Stock-Outs:**  
  Send sales, replacement, and purchase data to the API to get buffer margin and confidence scores.
- **Get Substitute Recommendations:**  
  Query the API with a product name or code to get semantic substitutes using RAG and LLM.
- **Automated Customer Communication:**  
  n8n triggers voice and text notifications using ElevenLabs and LLM.
- **AR-Guided Picking:**  
  Pickers use Snapchat Spectacles for guidance and AI for quality checks.
- **Claims Automation:**  
  Multimodal claims processed via n8n, LLM, and voice.

---

## Extending the Project

- Integrate SAP endpoints for real-time data.
- Add more n8n nodes for new business logic.
- Enhance ML models with additional features.
- Add dashboards for analytics and monitoring.

---

## Credits

Built for the Valio Aimo Junction 2025 hackathon by [Your Team Name].

---

## License

MIT License