<h1 align="center">
  🍔 BiteHub 
  <img src="https://res.cloudinary.com/dkdljnfja/image/upload/h_80/20251006_1824_Логотип_BiteHub_simple_compose_01k6x1yyrcf7m98mvtm5xexe78_y66vjd.png" alt="BiteHub Logo" height="35">
</h1>

<p align="center">
  <strong>BiteHub</strong> is a social platform for people who love cooking!<br>
  Share your recipes, leave reviews, discover new ideas, and get inspired by other users' culinary creations.<br>
  Built with <strong>Flask</strong>, easy to use, and ready to scale.
</p>

---

## 📝 Key Features

- Create, edit, and view recipes  
- Organize recipes with categories and ingredients  
- User reviews for recipes  
- JWT authentication and user roles (`Admin`, `User`)  
- Search, filters, and pagination for recipes  
- Upload recipe images via Cloudinary  
- Fully tested using **pytest**

---

## 🚀 Technologies

- **Backend:** Flask  
- **ORM:** SQLAlchemy + Alembic (migrations)  
- **Database:** PostgreSQL  
- **Authentication:** JWT  
- **Image Storage:** Cloudinary  
- **Testing:** pytest

---

## ⚙️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/BiteHub.git
cd BiteHub/backend_flask
```

### 2️⃣ Configure environment variables
Create a `.env` file in the `backend_flask` directory based on `.env.example`:
```bash
cp .env.example .env
```
Then edit `.env` file with your credentials.

### 3️⃣ Build and run with Docker
```bash
docker-compose build
docker-compose up
```
The application will be available at [http://localhost:5000](http://localhost:5000)

---

✅ Your BiteHub environment is now ready! Start creating recipes, registering users, and testing the API.