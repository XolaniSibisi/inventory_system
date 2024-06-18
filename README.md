# Farming E-commerce Inventory Management System

## Overview

FarmFresh Inventory Management System is a Django-based web application that helps manage inventory, orders, and invoicing for a farming business. Specializes in the sale of fruits, vegetables, and herbs. The system is designed to streamline the tracking and management of inventory, ensuring efficient operations and a seamless customer experience. 

## Features

### 1. Product Management

- Categorization of products based on types (fruits, vegetables, herbs), varieties, and other relevant criteria.
- Generation of unique SKUs (Stock Keeping Units) for each product.

### 2. Stock Tracking

- Real-time updates of stock levels.
- Low stock alerts to notify administrators.
- Batch tracking for improved traceability.

### 3. Order Management

- Integration with the order system for automatic stock adjustment.
- Real-time updates on order status (processing, shipped, delivered).
- Backorder management for out-of-stock items.

### 4. Reporting and Analytics

- Sales reports for different products, categories, and time periods.
- Inventory turnover rates for optimizing stock levels.

### 5. Barcode Scanning

- Use barcodes for quick and accurate product identification.

### 6. User Access and Permissions

- Different levels of access for employees to prevent unauthorized changes.

### 7. Mobile Accessibility

- Access inventory management functions on mobile devices.

### 8. Alerts and Notifications

- Receive alerts for low stock, or other critical events.

### 9. Returns and Refunds

- Manage product returns and update inventory levels accordingly.


### Prerequisites

- Installation of the latest python development kit from https://www.python.org/

## Project Setup
* Create an environment inside your project folder by running python<version> -m venv <virtual-environment-name>
* Activate the environment by running env/Scripts/activate.bat //In CMD
* Run the requirements file which has all the project dependencies using the $ pip install -r requirements.txt
* Run migrations to create tables inside the sqlite database by running $python manage.py makemigrations and python manage.py migrate
* Now run the application using $ python manage.py runserver command and copy and paste the localhost url http://127.0.0.1:8000/ to your browser. 


## Contributors

- Amogelang Monnanyana
- Musawenkosi Nyathi
- Xolani Sibisi
