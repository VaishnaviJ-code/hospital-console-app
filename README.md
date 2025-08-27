# Hospital Management Console App

A **console-based hospital management system** built with Python and MySQL.  
This project demonstrates OOP principles, database connectivity, and modular design.

---

## 🚀 Features
- User roles: Admin, Receptionist, Doctor, Pharmacist, Patient
- Patient registration and appointment scheduling
- Doctor diagnosis and prescription management
- Pharmacist medicine dispensing and inventory tracking
- Admin management of staff and system data
- Receptionist handling patient appointments and billing

---

## 🛠 Tech Stack
- **Language:** Python 3
- **Database:** MySQL
- **Libraries:** `mysql-connector-python`

---

## 📂 Project Structure
hospital-management/
│
├── hospital_app/ # Source code (Python modules)
│ ├── models/ # OOP classes for entities
│ ├── services/ # Business logic
│ ├── db/ # Database connection helpers
│ └── main.py # Entry point
│
├── tests/ # Unit tests
├── requirements.txt # Dependencies
├── .gitignore # Ignore unnecessary files
└── README.md # Project documentation


---

## ⚡ Setup & Run

1. Clone the repo:
   ```bash
   git clone https://github.com/VaishnaviJ-code/hospital-management.git
   cd hospital-management

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Linux/Mac
    venv\Scripts\activate      # On Windows

3. Install Dependencies

    ```bash
    pip install -r requirements.txt

4. Create MySQL database and update credentials in .env:

    ```env
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=yourpassword
    DB_NAME=hospital_db

5. Run the app:

    ```bash
    python hospital_app/main.py

## 👨‍💻 Author
    
    Developed by Visionaries

