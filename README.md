
# Cardano Cart API Endpoints

This document provides the design of API endpoints for the Cardano Cart ecommerce application. It covers all supported HTTP request methods for each entity, including Users, Products, Orders, Carts, Payments, and Reviews.

## General Information
- All endpoints are prefixed with `/api/v1`.
- Authentication is required for most endpoints, using Bearer tokens where necessary.
- Data is returned in JSON format.

---

## User Endpoints

### Register
- **POST** `/api/v1/users/register`
- **Description**: Register a new user.
- **Request Body**:
    ```json
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "first_name": "string",
        "last_name": "string",
        "address": "string",
        "phone_number": "string"
    }
    ```
- **Response**:
    ```json
    {	
	    "message": "Account created successfully",
	    "user": {
           "id": 1,
           "username": "string",
           "email": "string",
           "role": "customer",
           "created_at": "datetime"
        }
    }
    ```

### Login
- **POST** `/api/v1/users/login`
- **Description**: Authenticate a user.
- **Request Body**:
    ```json
    {
        "email": "string",
        "password": "string"
    }
    ```
- **Response**:
    ```json
    {
        "token": "jwt_token",
        "user": {
            "id": 1,
            "username": "string",
            "email": "string",
            "role": "customer"
        }
    }

    ```

### Get User Profile
- **GET** `/api/v1/users/{id}`
- **Description**: Retrieve user details by ID.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
        "id": 1,
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "address": "string",
        "phone_number": "string",
        "role": "customer",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
    ```

### Get all Users
- **GET** `/api/v1/users`
- **Description**: Retrieve all users
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    [
	    {
           "id": 1,
           "username": "string",
           "email": "string",
           "first_name": "string",
           "last_name": "string",
           "address": "string",
           "phone_number": "string",
           "role": "customer",
           "created_at": "datetime",
           "updated_at": "datetime"
    	}
    ]
    ```


### Update User Profile
- **PUT** `/api/v1/users/{id}`
- **Description**: Update user details.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "address": "string",
        "phone_number": "string"
    }
    ```
- **Response**:
    ```json
    {
	    "message": "User updated successfully",
	    "user": {
           "id": 1,
           "username": "string",
           "email": "string",
           "first_name": "string",
           "last_name": "string",
           "address": "string",
           "phone_number": "string",
           "updated_at": "datetime"
        }
    }
    ```

### Delete User
- **DELETE** `/api/v1/users/{id}`
- **Description**: Delete user account.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
        "message": "User deleted successfully."
    }
    ```

---

## Product Endpoints

### Add Product
- **POST** `/api/v1/products`
- **Description**: Add a new product.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "name": "string",
        "description": "string",
        "price": 0.0,
        "stock": 0,
        "category": "string",
        "images": ["string"]
    }
    ```
- **Response**:
    ```json
    {
	    "message": "Product added successfully",
	    "product": {
            "id": 1,
            "name": "string",
            "description": "string",
            "price": 0.0,
            "stock": 0,
            "category": "string",
            "images": ["string"],
	        "average_rating": 4.5,
            "created_at": "datetime"
       }
    }
    ```

### Get All Products
- **GET** `/api/v1/products`
- **Description**: Get all products.
- **Response**:
    ```json
    [
        {
            "id": 1,
            "name": "string",
            "description": "string",
            "price": 0.0,
            "stock": 0,
            "category": "string",
            "images": ["string"],
	        "average_rating": 4.5
        }
    ]
    ```

### Get Product by ID
- **GET** `/api/v1/products/{id}`
- **Description**: Get a product by its ID.
- **Response**:
    ```json
    {
        "id": 1,
        "name": "string",
        "description": "string",
        "price": 0.0,
        "stock": 0,
        "category": "string",
        "images": ["string"],
	    "average_rating": 4.5
    }
    ```

### Update Product
- **PUT** `/api/v1/products/{id}`
- **Description**: Update product details.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "name": "string",
        "description": "string",
        "price": 0.0,
        "stock": 0,
        "category": "string",
        "images": ["string"]
    }
    ```
- **Response**:
    ```json
    {
	    "message": "Product updated successfully",
	    "product": {
            "id": 1,
            "name": "string",
            "description": "string",
            "price": 0.0,
            "stock": 0,
            "category": "string",
            "images": ["string"],
	        "average_rating": 4.5,
            "updated_at": "datetime"
        }
    }
    ```

### Delete Product
- **DELETE** `/api/v1/products/{id}`
- **Description**: Delete a product.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
        "message": "Product deleted successfully."
    }
    ```

---

## Order Endpoints

### Get All Orders (Admin)
- **GET** `/api/v1/orders`
- **Description**: Get all orders.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    [
        {
            "id": 1,
            "buyer_id": 1,
            "shipping_address": "string",
            "total_amount": 0.0,
            "status": "pending",
            "tracking_number": "string"
        }
    ]
    ```

### Get Order by ID (Admin)
- **GET** `/api/v1/orders/{id}`
- **Description**: Get order details by ID.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
        "id": 1,
        "buyer_id": 1,
        "shipping_address": "string",
        "total_amount": 0.0,
        "status": "pending",
        "tracking_number": "string"
    }
    ```

### Create Order
- **POST** `/api/v1/{user_id}/orders`
- **Description**: Create a new order.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "buyer_id": 1,
        "shipping_address": "string",
        "total_amount": 0.0,
        "status": "pending",
        "tracking_number": "string"
    }
    ```
- **Response**:
    ```json
    {
	    "message": "Order created successfully",
	    "order": {
           "id": 1,
           "buyer_id": 1,
           "shipping_address": "string",
           "total_amount": 0.0,
           "status": "pending",
           "tracking_number": "string",
           "created_at": "datetime"
        }
    }
    ```

### Get all user Orders
- **GET** `/api/v1/{user_id}/orders`
- **Description**: Get all user orders.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    [
        {
            "id": 1,
            "buyer_id": 1,
            "shipping_address": "string",
            "total_amount": 0.0,
            "status": "pending",
            "tracking_number": "string"
        }
    ]
    ```
### Get user Order by ID

- **GET** `/api/v1/{user_id}/orders/{order_id}`
- **Description**: Get user order details by ID.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
        "id": 1,
        "buyer_id": 1,
        "shipping_address": "string",
        "total_amount": 0.0,
        "status": "pending",
        "tracking_number": "string"
    }
    ```


### Update Order
- **PUT** `/api/v1/{user_id}/orders/{order_id}`
- **Description**: update order.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "status": "completed"
    }
    ```
- **Response**:
    ```json
    {
	    "message": "Order updated successfully",
	    "order": {
            "id": 1,
            "buyer_id": 1,
            "shipping_address": "string",
            "total_amount": 0.0,
            "status": "completed",
            "tracking_number": "string",
            "created_at": "datetime",
	        "updated_at": "datetime"
        }
    }
    ```
---

## Cart Endpoints

### Add product to Cart
- **POST** `/api/v1/{user_id}/cart`
- **Description**: Add new item to cart.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "product_id": 1,
        "quantity": 1,
    }
    ```
- **Response**:
    ```json
    {
        "message": "Item added to cart successfully"
    }
    ```

### Remove product from Cart
- **DELETE** `/api/v1/{user_id}/cart/{product_id}`
- **Description**: Remove item from cart.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
        "message": "Item removed from cart successfully"
    }
    ```

### Update product in Cart
- **PUT** `/api/v1/{user_id}/cart/{product_id}`
- **Description**: Update item in cart.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "product_id": 1,
        "quantity": 2,
    }
    ```
- **Response**:
    ```json
    {
	    "message": "Item added to cart successfully",
	    "item":  {
           "product_id": 1,
           "quantity": 2,
    	} 
    }
    ```

### Get Cart
- **GET** `/api/v1/{user_id}/cart`
- **Description**: View Cart.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    { 
       "items": [
           {
               "product_id": 1,
               "quantity": 1,
           }
       ],
       "total_price": 10.99
    }
    ```

### Checkout Cart
- **POST** `/api/v1/{user_id}cart/checkout`
- **Description**: Checkout Cart.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
	    "message": "Checkout Successful"
    }
    ```

## Payment Endpoints
### Initiate Payment
- **POST** `/api/v1/payment`
- **Description**: Initiate payment for an order.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "order_id": 1,
        "amount": 10.99,
    }
    ```
- **Response**:
    ```json
    {
        "payment_id": 1,
        "qr_code": "link",
        "status": "pending",
        "created_at": "datetime"
    }
    ```

### Update Payment Status
- **PUT** `/api/v1/payment/{payment_id}`
- **Description**: Update payment status.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "status": "completed",
    }
    ```
- **Response**:
    ```json
    {
	    "message": "Payment status updated successfully",
	    "payment": {
            "payment_id": 1,
            "status": "completed",
            "created_at": "datetime",
	        "updated_at": "datetime"
        }
    }
    ```

## Review Endpoints

### Add a Review
- **POST** `/api/v1/{product_id}/reviews`
- **Description**: Add a review for a product.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
        "user_id": 1,
	    "product_id": 1,
	    "rating": 4,
        "comment": "Great product!",
    }
    ```
- **Response**:
    ```json
    {
        "message": "Review added successfully"
    }
    ```

### Update a Review
- **PUT** `/api/v1/{product_id}/reviews/{review_id}`
- **Description**: Update a review for a product.
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
    ```json
    {
	    "rating": 5,
        "comment": "Even a better product than I thought!",
    }
    ```
- **Response**:
    ```json
    {
        "message": "Review updated successfully",
	    "product": {	
	        "review_id": 1,
	        "user_id": 1,
	        "product_id": 1,
	        "rating": 5,
            "comment": "Even a better product than I thought!",
	        "created_at": "datetime",
	        "updated_at": "datetime"
        }
    }
    ```

### Delete a Review
- **DELETE** `/api/v1/{product_id}/reviews/{review_id}`
- **Description**: Delete a review for a product.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {
        "message": "Review deleted successfully"
    }
    ```

### Get Review by ID
- **GET** `/api/v1/{product_id}/reviews/{review_id}`
- **Description**: Get a review for a product.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    {	
	    "review_id": 1,
	    "user_id": 1,
	    "product_id": 1,
	    "rating": 4,
        "comment": "Great product!",
	    "created_at": "datetime"
    }
    ```

### Get all Reviews
- **GET** `/api/v1/{product_id}/reviews`
- **Description**: Get all reviews.
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
    ```json
    [
	    {	
	        "review_id": 1,
	        "user_id": 1,
	        "product_id" 1,
	        "rating": 4,
            "comment": "Great product!",
	        "created_at": "datetime"
        }
    ]
    ```

