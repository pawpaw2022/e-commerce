# E-Commerce Dashboard

A full-stack e-commerce analytics dashboard built with FastAPI and Streamlit. This application provides a comprehensive interface for managing and analyzing e-commerce data including products, categories, customers, orders, and reviews.

## Features

- **Products Management**: Add, view, and delete products with category assignments and pricing
- **Categories Management**: Organize products with customizable categories
- **Customer Management**: Track customer information and purchasing history
- **Order Analytics**: View and analyze order data with rich visualizations
- **Review System**: Manage and analyze product reviews and ratings
- **Interactive Dashboard**: Filter and visualize data with real-time updates
- **Responsive Design**: Clean and modern interface that works across devices

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: MySQL
- **Data Processing**: Pandas
- **Visualization**: Streamlit built-in charts

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/pawpaw2022/e-commerce.git
cd e-commerce
```

2. Create and activate a virtual environment:

```bash

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

```


3. Install required packages:

```bash
pip install -r requirements.txt
```


4. Configure MySQL:
   - Create a MySQL database named `ecommerce`
   - Update database credentials in `app/db/config.py` or use environment variables:
     ```
     MYSQL_USER=your_username
     MYSQL_PASSWORD=your_password
     MYSQL_HOST=localhost
     MYSQL_PORT=3306
     MYSQL_DB=ecommerce
     ```

5. Initialize the database:
   - Run the SQL script to create tables and sample data:
     ```bash
     mysql -u your_username -p ecommerce < app/db/ecommerce.sql
     ```

## Running the Application

1. Start the FastAPI backend:

```bash
cd app
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`

2. Start the Streamlit frontend (in a new terminal):

```bash

streamlit run streamlit_app.py

```

The dashboard will be available at `http://localhost:8501`

## API Documentation

Once the backend is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Environment Variables

The application uses the following environment variables:

- `API_URL`: Backend API URL (default: `http://localhost:8000`)
- `MYSQL_USER`: Database username
- `MYSQL_PASSWORD`: Database password
- `MYSQL_HOST`: Database host
- `MYSQL_PORT`: Database port
- `MYSQL_DB`: Database name


