### 📈 Stock Tracker Web App  
A **Flask-based stock tracking web application** that allows users to monitor stock prices, visualize trends, and receive automated email notifications.  

## 🚀 Features  
- **Stock Watchlist**: Add/remove stocks and track their performance.  
- **Real-time Stock Data**: Uses **Finnhub & Alpha Vantage APIs**.  
- **Stock Visualization**: Interactive **Plotly** charts.  
- **Automated Email Reports**: Daily stock summary via **Flask-Mail & APScheduler**.  
- **Live Alerts**: Get notified when a stock price changes significantly.  
- **User Authentication**: Secure login/logout using **Flask-Login & Flask-Bcrypt**.  
- **Optimized Performance**: API call & DB query optimizations.  
- **Dockerized Deployment**: Runs in a **Docker container** with **Celery & Redis**.  

---

## 🛠️ Installation  

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-username/stock-tracker.git
cd stock-tracker
```

### **2. Set Up a Virtual Environment (Optional but Recommended)**  
Using **Poetry**:  
```bash
poetry install
poetry shell
```
Or using **venv**:  
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**  
Create a `.env` file in the project root:  
```ini
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost/stock_db
FINNHUB_API_KEY=your_finnhub_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

### **4. Run Database Migrations**  
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### **5. Start the Flask App**  
```bash
flask run
```
App will run at: **http://127.0.0.1:5000/**  

---

## 🐳 Docker Deployment  
### **1. Build & Run Docker Containers**  
```bash
docker-compose up --build
```
This will start:  
- Flask app  
- PostgreSQL  
---

## 📊 Stock Data Visualization  
- **Live Updating Line Chart** (Real-time stock price trend).  
- **Bar Chart** (Stock price comparison: Open, High, Low, Close).  
- **Gauge Chart** (Price change percentage).  

---

## 🔐 User Authentication  
- **Flask-Login** for user sessions.  
- **Flask-Bcrypt** for secure password hashing.  

---

## 📩 Automated Email System  
- **Flask-Mail** sends emails to users.  
- **APScheduler** schedules daily reports.  
---

## 📜 API Integration  
- **Finnhub API**: Fetches real-time stock data.  
- **Alpha Vantage API**: Used for historical data & indicators.  

---

## 🛠️ Tech Stack  
| Technology      | Purpose                         |  
|---------------|---------------------------------|  
| Flask         | Web framework                   |  
| PostgreSQL    | Database                        |  
| TailwindCSS   | Frontend styling                |  
| Chart.js      | Stock price charts              |  
| Plotly        | Interactive stock data visualization |  
| Flask-Mail    | Email notifications             |  
| APScheduler   | Scheduled jobs (daily reports)  |  
| Docker        | Containerized deployment        |  

---

## 📝 Future Improvements  
- Implement WebSockets for real-time updates.  
- Add stock market news & sentiment analysis.  
- Improve UI/UX with better TailwindCSS components.  

---

## 🎯 Contributing  
Pull requests are welcome! Feel free to submit issues and suggestions.  

---

## 📄 License  
MIT License.  

---

## 💬 Questions?  
Feel free to reach out! 🚀
