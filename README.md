# file-sharing-system

# 🔐 Secure File Sharing System – Backend

This is a secure file-sharing backend system built with **Flask** for **role-based access**:
- 📥 **Ops Users** can upload `.docx`, `.pptx`, `.xlsx` files
- 📤 **Client Users** can securely view and download those files
- 🛡️ Authenticated via JWT and role-restricted API access

---

## 🚀 Features

✅ Client & Ops user registration/login  
✅ JWT-based authentication  
✅ Role-based access (Client / Ops)  
✅ Secure file upload (Ops only)  
✅ Encrypted download links (Client only)  
✅ SQLite database  
✅ Clean modular code structure  
✅ Fully testable with Pytest

---

## 🛠️ Tech Stack

| Layer        | Tech Used           |
|--------------|---------------------|
| Backend      | Python, Flask       |
| Database     | SQLite, SQLAlchemy  |
| Auth         | Flask-JWT-Extended  |
| Passwords    | Flask-Bcrypt        |
| Encryption   | ItsDangerous        |
| Email (Optional) | Flask-Mail     |
| Testing      | Pytest              |

---

## 📁 Folder Structure

file-sharing-system/
│
├── app/
│ ├── init.py
│ ├── config.py
│ ├── models.py
│ ├── routes/
│ │ ├── auth_routes.py
│ │ ├── ops_routes.py
│ │ ├── client_routes.py
│ ├── utils/
│ ├── role_required.py
│ ├── encryption.py
│
├── uploads/ # Uploaded files
├── site.db # SQLite DB
├── run.py # App entry point
├── requirements.txt
├── .env
└── tests/
└── test_auth.py

/auth/login
→ Login client or ops and receive access token

/ops/upload
→ Upload .docx/.pptx/.xlsx (Only for Ops)
→ Requires header:
Authorization: Bearer <access_token>

/client/files
→ Get secure download links (Only for Client)

/client/download?token=...
→ Download a file with encrypted token

🧪 Running Tests
bash
Copy
Edit
pytest
📦 Setup Instructions
bash
Copy
Edit
git clone https://github.com/yourusername/file-sharing-system.git
cd file-sharing-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python
>>> from app import create_app, db
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
python run.py
Author
Chitransha Bhatt



