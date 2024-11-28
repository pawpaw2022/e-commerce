import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from urllib.parse import urlencode

# API base URL
API_URL = "http://localhost:8000"

def main():
    st.title("E-Commerce Dashboard")
    
    # Get current page from URL parameters
    current_page = st.query_params.get("page", "Products")
    
    # Sidebar navigation with URL updates
    pages = ["Products", "Categories", "Customers", "Orders", "Reviews"]
    page = st.sidebar.selectbox(
        "Select Page",
        pages,
        index=pages.index(current_page)
    )
    
    # Update URL when page changes using the new method
    st.query_params["page"] = page
    
    if page == "Products":
        show_products_page()
    elif page == "Categories":
        show_categories_page()
    elif page == "Customers":
        show_customers_page()
    elif page == "Orders":
        show_orders_page()
    elif page == "Reviews":
        show_reviews_page()

def show_products_page():
    st.header("Products")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        category_id = st.number_input("Category ID", min_value=0, step=1)
    with col2:
        min_price = st.number_input("Min Price", min_value=0.0, step=0.01)
    with col3:
        max_price = st.number_input("Max Price", min_value=0.0, step=0.01)
    
    # Get products with filters
    params = {}
    if category_id > 0:
        params['category_id'] = category_id
    if min_price > 0:
        params['min_price'] = min_price
    if max_price > 0:
        params['max_price'] = max_price
    
    response = requests.get(f"{API_URL}/products", params=params)
    if response.status_code == 200:
        products = response.json().get('products', [])
        if products:
            df = pd.DataFrame(products)
            st.dataframe(df)
        else:
            st.info("No products found")
    else:
        st.error("Failed to fetch products")

def show_categories_page():
    st.header("Categories")
    
    response = requests.get(f"{API_URL}/categories")
    if response.status_code == 200:
        categories = response.json().get('categories', [])
        if categories:
            df = pd.DataFrame(categories)
            st.dataframe(df)
        else:
            st.info("No categories found")
    else:
        st.error("Failed to fetch categories")

def show_customers_page():
    st.header("Customers")
    
    # Filters
    state = st.text_input("Filter by State")
    
    # Get customers with filters
    params = {}
    if state:
        params['state'] = state
    
    response = requests.get(f"{API_URL}/customers", params=params)
    if response.status_code == 200:
        customers = response.json().get('customers', [])
        if customers:
            df = pd.DataFrame(customers)
            st.dataframe(df)
        else:
            st.info("No customers found")
    else:
        st.error("Failed to fetch customers")

def show_orders_page():
    st.header("Orders")
    
    # Add a toggle for filters
    show_filters = st.expander("Show Filters", expanded=False)
    
    with show_filters:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=None)
        with col2:
            end_date = st.date_input("End Date", value=None)
        
        customer_id = st.number_input("Customer ID", min_value=0, step=1)
    
    # Get orders with filters
    params = {}
    if customer_id > 0:
        params['customer_id'] = customer_id
    if start_date:
        params['start_date'] = start_date.strftime('%Y-%m-%d')
    if end_date:
        params['end_date'] = end_date.strftime('%Y-%m-%d')
    
    # Show loading message while fetching data
    with st.spinner('Loading orders...'):
        response = requests.get(f"{API_URL}/orders", params=params)
        if response.status_code == 200:
            orders = response.json().get('orders', [])
            if orders:
                # Create caches for customer and product data
                customer_cache = {}
                product_cache = {}
                enriched_orders = []
                
                # Get unique customer and product IDs
                customer_ids = set(order['customerId'] for order in orders)
                product_ids = set(order['productId'] for order in orders)
                
                # Prefetch all unique customer data
                for cust_id in customer_ids:
                    customer_response = requests.get(f"{API_URL}/customers/{cust_id}")
                    if customer_response.status_code == 200:
                        customer_cache[cust_id] = customer_response.json()
                
                # Prefetch all unique product data
                for prod_id in product_ids:
                    product_response = requests.get(f"{API_URL}/products/{prod_id}")
                    if product_response.status_code == 200:
                        product_cache[prod_id] = product_response.json()
                
                # Process orders using cached data
                for order in orders:
                    customer = customer_cache.get(order['customerId'])
                    product = product_cache.get(order['productId'])
                    
                    enriched_order = {
                        'Order ID': order['orderId'],
                        'Order Date': order['orderDate'],
                        'Quantity': order['quantity'],
                        'Customer ID': order['customerId'],
                        'Customer Name': f"{customer['firstName']} {customer['lastName']}" if customer else "Unknown",
                        'Customer State': customer['addressState'] if customer else "Unknown",
                        'Product ID': order['productId'],
                        'Product Name': product['productName'] if product else "Unknown",
                        'Product Price': product['price'] if product else 0,
                        'Total Amount': order['quantity'] * float(product['price']) if product else 0
                    }
                    enriched_orders.append(enriched_order)
                
                # Convert to DataFrame
                df = pd.DataFrame(enriched_orders)
                
                # Show order statistics
                st.subheader("Order Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Orders", len(df))
                with col2:
                    st.metric("Total Items", df['Quantity'].sum())
                with col3:
                    st.metric("Total Revenue", f"${df['Total Amount'].sum():.2f}")
                
                # Show orders table
                st.subheader("Orders Details")
                st.dataframe(
                    df,
                    column_config={
                        "Total Amount": st.column_config.NumberColumn(
                            "Total Amount",
                            format="$%.2f"
                        ),
                        "Product Price": st.column_config.NumberColumn(
                            "Product Price",
                            format="$%.2f"
                        )
                    }
                )
                
                # Show charts
                st.subheader("Order Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Orders by state
                    st.caption("Orders by State")
                    state_orders = df['Customer State'].value_counts()
                    st.bar_chart(state_orders)
                    
                with col2:
                    # Top products
                    st.caption("Top Products by Order Quantity")
                    product_orders = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False)
                    st.bar_chart(product_orders)
                
            else:
                st.info("No orders found")
        else:
            st.error("Failed to fetch orders")

def show_reviews_page():
    st.header("Reviews")
    
    # Add a toggle for filters
    show_filters = st.expander("Show Filters", expanded=False)
    
    with show_filters:
        # Rating filters
        col1, col2 = st.columns(2)
        with col1:
            min_rating = st.slider("Min Rating", 1, 10, 1)
        with col2:
            max_rating = st.slider("Max Rating", 1, 10, 10)
        
        # ID filters
        col3, col4 = st.columns(2)
        with col3:
            product_id = st.number_input("Product ID", min_value=0, step=1)
        with col4:
            customer_id = st.number_input("Customer ID", min_value=0, step=1)
    
    # Get reviews with filters
    params = {}
    if product_id > 0:
        params['product_id'] = product_id
    if customer_id > 0:
        params['customer_id'] = customer_id
    params['min_rating'] = min_rating
    params['max_rating'] = max_rating
    
    with st.spinner('Loading reviews...'):
        response = requests.get(f"{API_URL}/reviews", params=params)
        if response.status_code == 200:
            reviews = response.json().get('reviews', [])
            if reviews:
                # Create caches for customer and product data
                customer_cache = {}
                product_cache = {}
                enriched_reviews = []
                
                # Get unique customer and product IDs
                customer_ids = set(review['customerId'] for review in reviews)
                product_ids = set(review['productId'] for review in reviews)
                
                # Prefetch all unique customer data
                for cust_id in customer_ids:
                    customer_response = requests.get(f"{API_URL}/customers/{cust_id}")
                    if customer_response.status_code == 200:
                        customer_cache[cust_id] = customer_response.json()
                
                # Prefetch all unique product data
                for prod_id in product_ids:
                    product_response = requests.get(f"{API_URL}/products/{prod_id}")
                    if product_response.status_code == 200:
                        product_cache[prod_id] = product_response.json()
                
                # Process reviews using cached data
                for review in reviews:
                    customer = customer_cache.get(review['customerId'])
                    product = product_cache.get(review['productId'])
                    
                    enriched_review = {
                        'Review ID': review['reviewId'],
                        'Rating': review['rating'],
                        'Customer ID': review['customerId'],
                        'Customer Name': f"{customer['firstName']} {customer['lastName']}" if customer else "Unknown",
                        'Customer State': customer['addressState'] if customer else "Unknown",
                        'Product ID': review['productId'],
                        'Product Name': product['productName'] if product else "Unknown",
                        'Product Price': product['price'] if product else 0
                    }
                    enriched_reviews.append(enriched_review)
                
                # Convert to DataFrame
                df = pd.DataFrame(enriched_reviews)
                
                # Show review statistics
                st.subheader("Review Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Reviews", len(df))
                with col2:
                    avg_rating = df['Rating'].mean()
                    st.metric("Average Rating", f"{avg_rating:.1f}⭐")
                with col3:
                    five_star_percent = (df['Rating'] >= 8).mean() * 100
                    st.metric("High Ratings (8-10)", f"{five_star_percent:.1f}%")
                
                # Add rating visualizations
                st.subheader("Rating Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Rating Distribution
                    st.caption("Rating Distribution")
                    rating_counts = df['Rating'].value_counts().sort_index()
                    st.bar_chart(rating_counts)
                
                with col2:
                    # Average Rating by Product
                    st.caption("Average Rating by Product")
                    product_ratings = df.groupby('Product Name')['Rating'].mean().sort_values(ascending=False)
                    st.bar_chart(product_ratings)
                
                # Show detailed reviews table
                st.subheader("Reviews Details")
                st.dataframe(
                    df,
                    column_config={
                        "Rating": st.column_config.NumberColumn(
                            "Rating",
                            format="%.1f ⭐"
                        ),
                        "Product Price": st.column_config.NumberColumn(
                            "Product Price",
                            format="$%.2f"
                        )
                    }
                )
                
                # Additional insights
                st.subheader("Review Insights")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Reviews by State
                    st.caption("Reviews by State")
                    state_reviews = df['Customer State'].value_counts()
                    st.bar_chart(state_reviews)
                
                with col2:
                    # Most Active Reviewers
                    st.caption("Most Active Reviewers")
                    reviewer_counts = df['Customer Name'].value_counts().head(10)
                    st.bar_chart(reviewer_counts)
                
            else:
                st.info("No reviews found")
        else:
            st.error("Failed to fetch reviews")

if __name__ == "__main__":
    main() 