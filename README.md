# DealsShare

DealsShare is a web-based platform for managing and sharing products and deals.  
Users can register, log in, add products, save items to favorites, and view their personal profile.  
The system also includes an Admin Panel for managing users and products.

---

## Features

### Users
- Register and log in to the system  
- Browse all products or view a single product  
- Add new products  
- Save products to favorites  
- View and edit personal profile  

### Admin
- View and manage all users  
- Full control over products  
- Update or delete products and users  

---

## Technologies
- Backend: Flask (Python)  
- Frontend: HTML, CSS, Jinja2  
- Database: SQLite (can be extended to PostgreSQL/MySQL)  
- Tools: VScode, GitHub  

---

## Installation & Run

1. Clone the repository:
   ```bash
   git clone https://github.com/YehudaWieder/DealsShare.git
   cd DealsShare

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt

  3. Run the server:
     ```bash
       python3 app.py
     ```
     
---

## Project Structure
   
   ```bash
      DealsShare/
      │── app.py               # Main application entry point
      │── /routes              # Routes (users, products, admin)
      │── /templates           # HTML templates (Jinja2)
      │── /static              # CSS, JS, images
      │── /database            # CRUD operations + SQL scripts
      │── requirements.txt     # Project dependencies
      │── README.md            # Project documentation
   