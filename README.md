# Django Auctions Project

This is a web application developed using Django for online auctions. Users can create listings, place bids, add items to their watchlist, comment, and participate in the auction process. This was the Project 2 of the CS50W course.

## Features

- User authentication (Login, Logout, Registration)
- Create, edit, and close auction listings
- Place bids on listings
- Add and remove listings from the watchlist
- Comment on auction listings
- Browse listings by category

## Technologies Used

- Python 3.11.4
- Django 5.0.1
- HTML, CSS
- Bootstrap
- SQLite

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Aply database migrations:

   ```bash
    python manage.py migrate
   ```
3. Run the development server:

    ```bash
    python manage.py runserver
    ```
The application will be accessible at http://127.0.0.1:8000/

## Usage

1. Create a super user in django

    ```bash
    python manage.py createsuperuser
    ```
    
2. Login to the admin panel at http://127.0.0.1:8000/admin/ to manage categories, users, and listings.

3. Use the web application to create listings, place bids, and explore the auction features.


## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add a new feature'`
4. Push the branch: `git push origin feature-name`
5. Create a pull request.

   
   
