# Customer_Support_Chatbot
An intelligent customer support chatbot built using LangChain, OpenAI, and RAG that automatically understands user intent and responds accurately using both knowledge-base retrieval and real-time order information from the database.




A production-ready customer support assistant built using **LangChain**, **FAISS**, **OpenAI**, and **Supabase**.
This chatbot can:

✅ Answer questions from **uploaded docs** (RAG)
✅ Answer questions from **database** (order details)
✅ Classify customer intent (normal, irrelevant, order ID)
✅ Retrieve relevant chunks using **FAISS vector store**
✅ Handle conversation flow using **LangChain RunnableBranch**


---

## 📌 Features

### 🔍 1. Smart Intention Classification

The bot understands the user's intent:

* **normal** → services, pricing, FAQs
* **order_id** → requests order details
* **irrelevant** → greetings, weather, personal chat

### 📄 2. RAG-Based Company Info Answering

The chatbot loads your service documents, splits them, embeds them, and stores vectors in FAISS.

It retrieves the most relevant chunks when answering.

### 🗄 3. Order Lookup From Supabase

Users can ask:

> “What is the status of my order 12?”

The bot extracts the order ID, fetches data from Supabase, and replies with a one-line summary.

---

## 📁 Project Folder Structure

```
customer-support-chatbot/
│
├── main.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
|   └── knowledge_base/
|        └── company_overview.pdf
|        └── FAQ.pdf
|        └── Services.pdf
|        └── Refund_Policy.pdf
│   └── vector_backup/
│       └── embedding_backup.json
│
├── prompts/
│   ├── __init__.py
│   ├── prompt_intention.py
│   ├── prompt_normal.py
│   ├── prompt_order.py
│   └── prompt_irrelevant.py
│
├── schemas/
│   ├── __init__.py
│   └── intention_schema.py
│
├── services/
│   ├── __init__.py
│   ├── llm_service.py
│   ├── db_service.py
│   └── vector_service.py
│
├── chains/
│   ├── __init__.py
│   └── router_chain.py
│
├── utils/
│   ├── __init__.py
│   └── history.py
│


```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/customer-support-chatbot.git
cd customer-support-chatbot
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Add environment variables

Create a **.env** file:

```
OPENAI_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_API_KEY=your_key

```

---




## 🧠 How It Works (Architecture)

### 1. User message → Intention Classifier (Pydantic Output Parser)

### 2. Based on intent:

* **normal** → Search FAISS → answer using RAG
* **order_id** → Query Supabase → return details
* **irrelevant** → Greeting or polite redirect

### 3. Chatbot returns final answer

---

## Future Improvement

## 📬 Email Escalation (New Feature)

When chatbot cannot answer:

✔ Sends email to support
✔ Includes:

* User message
* Retrieved chunks
* Full conversation
* Confidence score (optional)

✔ User gets reply:

> "I have forwarded your query to our support staff. They will contact you soon."

---

## 🖥 Upcoming Improvements

✅ Add analytics dashboard (customer queries, intents, order lookups)
✅ Improve order details formatting
✅ Add streaming responses
✅ Add chat-ticket history system

---


## Output CLI 



<img width="1131" height="473" alt="Screenshot 2025-12-05 130035" src="https://github.com/user-attachments/assets/7ce703db-e5cc-4b28-9280-86fe044cead6" />
