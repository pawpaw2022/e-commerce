# intermediate-python-final-project


## Project idea: Online shopping API

I would like to create an API that facilitates online shopping by providing essential features to support both buyers and sellers. The API will include methods to:

- Return a list of available products by category, brand, or price range, pulling data from a product database.
- Take in a product ID and return detailed information about the product, including specifications, images, and customer reviews.
- Allow users to search for products by name or keyword, and sort the results by relevance, price, or popularity.
- Take in a user ID and return their shopping cart contents, including the total price and any applicable discounts.
- Integrate with a payment gateway API (such as Stripe or PayPal) to process payments securely.
- Allow for the addition, update, and removal of products by sellers, including setting prices, managing stock levels, and uploading product images.

Generate order details, allowing users to track the status of their orders through shipping information updates.
I will first focus on building the core methods, then integrate them into an API using FastAPI or Flask, allowing external clients to interact with the shopping system through HTTP requests.


## Online Shopping API Project Plan

### By the end of Week 4:
- Research API frameworks, and decide whether to use FastAPI or Flask.
- Set up the project environment, including installing necessary libraries.
- Create the basic API structure that can handle HTTP requests and return basic responses (e.g., "Hello World" or a test endpoint).

### By the end of Week 5:
- Build the database schema to store products, users, and orders.
- Implement methods to return a list of available products by category, brand, or price range.
- Add functionality to return detailed product information based on a product ID.

### By the end of Week 6:
- Create methods that allow users to search for products by name or keyword and sort results by relevance, price, or popularity.
- Implement the user shopping cart, with methods to return shopping cart contents, total prices, and any applicable discounts.
- Ensure the database is updated properly when items are added or removed from the cart.

### By the end of Week 7:
- Integrate with a payment gateway (e.g., Stripe or PayPal) to securely process payments.
- Implement methods to allow sellers to add, update, and remove products, including managing stock levels and uploading images.
- Build out product image handling and specifications management.

### By the end of Week 8:
- Implement order generation and tracking, allowing users to view and track the status of their orders.
- Finalize the integration of the API, ensuring that all core methods are functional.
- Start writing API documentation for external clients to use the system.

### By the end of Week 9:
- Conduct thorough testing of all endpoints (unit tests, integration tests, etc.).
- Improve error handling and add appropriate response codes (400, 404, 500, etc.).
- Optimize the API performance by tuning database queries and reducing response times.

### By the end of Week 10:
- Finalize project documentation, including setup instructions, usage examples, and API endpoint descriptions.
- Polish the codebase by refactoring and ensuring it adheres to best practices.
- Prepare and record a demo video showcasing key features of the API.
