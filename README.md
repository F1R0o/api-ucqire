# 🎬 UCQIRE API

A clean, professional **Flask REST API** for a movie and TV series platform.

✅ **Pure Flask** (no SQLAlchemy)  
✅ **Raw SQLite3** database  
✅ **Modular Blueprint architecture**  
✅ **JSON APIs only** (no HTML templates)  
✅ **Production-ready** setup with environment configs

---

## 🚀 Features

- **Authentication**: Login, Logout, Create Admins
- **Movies Module**: List, Search, Filter, Sort by views/date
- **Series Module**: List, Search, Filter Series and Episodes
- **Upload Module**: Upload Movies, Series, Episodes via API
- **Admin Module**: View analytics, manage admins
- **Real-time Ready**: Flask-SocketIO integrated
- **CORS Enabled**: Ready for frontend/backend integration

---

## 🛠 Technologies

- Python 3.10+
- Flask
- Flask-CORS
- Flask-SocketIO
- SQLite3 (raw)
- dotenv (for environment variables)

---

## 📦 Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ucqire-api.git
    cd ucqire-api
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install the requirements**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    python run.py
    ```

App will start on `http://127.0.0.1:5000/`

---

## ⚙️ Environment Variables (.env)

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key
