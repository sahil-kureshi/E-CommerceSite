# E-CommerceSite
I'm building an E-Commerce website like Flipkart. Consisting of sign-up, login functionality seperated normal user and Admin user. People can go to front end shop products, add to cart, pay using payment gateway and get payment confirmation. Users can also track product's delivery status. Front-End written in React and Back-End in Python (FastApi).



# 🥿 Sahil Footwear E‑Commerce

A full‑stack footwear e‑commerce application built with **React + FastAPI + MySQL**, featuring secure JWT authentication and Razorpay payment integration.

---

## 🚀 Features
- 👟 Product catalog with CRUD operations
- 🛒 Shopping cart and order management
- 🔑 JWT‑based signup/login
- 💳 Razorpay payment gateway integration
- 📦 Modular backend with FastAPI routers
- 🎨 Modern React frontend (Vite)

---

## 📂 Project Structure
frontend/         # React app
backend/
├── main.py       # FastAPI entrypoint
├── database.py   # SQLAlchemy session + Base
├── models.py     # ORM models
├── schemas.py    # Pydantic schemas
├── config.py     # Environment variables
└── routers/      # Modular API routers
├── products.py
├── orders.py
├── payments.py
└── auth.py


Code
---

## ⚙️ Installation

### Backend
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/footwear-site.git
   cd footwear-site/backend
   

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows


3. Install dependencies:
   ```bash
   pip install -r requirements.txt


4. Configure environment variables in .env
   code
   DATABASE_URL=mysql+pymysql://user:password@localhost/footwear_db
   JWT_SECRET=your_secret_key
   JWT_ALGORITHM=HS256
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret                                                                  


5. Run the server:
   ```bash
   uvicorn main:app --reload


**Frontend**

1. Navigate to frontend:
   ```bash
   cd ../frontend

2. Install dependencies:
   ```bash
   npm install

3. Start development server:
   ```bash
   npm run dev


📖 **Author**
   Developed by **Sahil** — Entrepreneur, Full Stack Developer, and Data Engineer.
   Location: India.
   Focus: Scalable e‑commerce systems, AI‑driven automation, secure payment integration.
