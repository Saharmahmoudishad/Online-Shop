# Online Shop django Project
## overview
This project is an online shop developed using Django, a high-level Python web framework. It encompasses various functionalities essential for an e-commerce platform.

## Project Structure
- **core**: The core app serves as the heart of our online shop, handling essential features that are shared across multiple parts of the application. This includes models such as discounts, vouchers, city and province information, images, comments, and more. Additionally, the core app acts as a central repository for functionalities that don't neatly fit into other specific apps but are crucial for the overall functionality of the platform.
- **customers**: The customers app is responsible for managing all users, including staff and regular customers, as well as their associated data and profiles.
- **product**: The product app focuses on product management, including adding new products, managing inventory, and showcasing product details.
- **orders**: This app handles order processing, from creating and managing orders to tracking shipment status and order history.
...

## Django Rest Framework (DRF)
Part of this project is handled using Django Rest Framework (DRF), a powerful toolkit for building Web APIs in Django.

### Cart
The cart functionality manages the user's shopping cart, allowing them to add, remove, and update items before proceeding to checkout.

### Checkout
The checkout process facilitates the completion of the purchase, including selecting shipping options, entering billing information, and confirming the order.

### Customer Profile
The customer profile section provides users with access to their account information, order history, and preferences.

Cart and Checkout
The cart and checkout functionalities are seamlessly integrated into the order management process, allowing users to add items to their cart, proceed to checkout, and complete their purchases securely.


## Project Setup
Before running the project, make sure to install the required Python packages listed in the requirements.txt file. You can do this by executing the following command:

```bash
Copy code
pip install -r requirements.txt
```
This command will install all the necessary dependencies for the project to run successfully.

## Technologies Used
Database: PostgreSQL is utilized as the primary database backend, offering reliability, scalability, and robust features for storing and managing data.

Caching: Redis is employed for caching purposes, enhancing performance and reducing latency by storing frequently accessed data in memory.

Task Queue: Celery is integrated into the project for handling asynchronous tasks such as sending emails. By offloading time-consuming tasks to Celery workers, the main application can remain responsive and efficient.

## Entity-Relationship Diagram (ERD)
You can visualize the database schema of the project using the Entity-Relationship Diagram (ERD) available at the following link:
[ERD PDF](https://dbdiagram.io/d/656c217d56d8064ca044e198)
**you can find pdf of ERD PDF in Doc directory of project**

This ERD provides an overview of the database structure and relationships between different entities in the project.

## Project Configuration
To run the project, you need to set up the configuration using the provided INI file. Follow these steps:

- **Database Configuration**:
Update the [database] section in the config.ini file with your PostgreSQL database details. Modify the following parameters as per your setup:

ENGINE: Database engine (e.g., django.db.backends.postgresql).
NAME: Name of the database (e.g., Online_Shop).
USER: Database username (e.g., postgres).
PASSWORD: Database password.
PORT: Database port (default is 5432).
HOST: Database host (e.g., localhost).
Email Configuration:
Update the [email_data] section with your email configuration details. Ensure you have a valid SMTP server set up. Modify the following parameters:

EMAIL_BACKEND: Django email backend.
EMAIL_HOST: SMTP server host (e.g., smtp.gmail.com).
EMAIL_HOST_USER: Your email address.
EMAIL_PORT: SMTP server port (e.g., 587).
EMAIL_HOST_PASSWORD: Your email account password.
EMAIL_USE_TLS: Enable TLS (set to True).
DEFAULT_FROM_EMAIL: Default sender email address.
- **Google OAuth2 Configuration**:
Update the [gmail_login] section with your Google OAuth2 credentials. These are used for social authentication with Google services. Modify the following parameters:

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: Google OAuth2 client ID.
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: Google OAuth2 client secret.
- **SMS Configuration**:
Update the [sending_sms] section with your SMS API credentials and phone number. Modify the following parameters:

APIKey: Your SMS API key.
phonenumber: Your phone number for sending SMS notifications.
Once you've updated the config.ini file with your configuration details, you can proceed to run the project using the provided instructions in the README.

Once you've completed the configuration, you can proceed to run the project using the following command:

```python
python manage.py runserver
```
This will start the Django development server, and your project will be accessible at the specified URL.

Running Redis and Celery for Celery Task Management
To utilize Celery for task management, you need to first start Redis and then run Celery. Execute the following commands in order:

## Run the Django Server:


```python
python manage.py runserver
```
### Start the Redis Server:
Before using Celery, ensure that the Redis server is running. Depending on how Redis is installed and configured, you may use different commands for this purpose. Typically, you can use the following command:


```bash
redis-server
```
### Run Celery Workers:


```bash
python -m celery -A django_celery worker
```
This command starts Celery workers as part of your system. This way, Celery is ready to handle tasks in the background.

By following these steps, the Celery environment is ready for use, and you can utilize it to manage various tasks within your project.


