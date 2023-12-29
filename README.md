Flask Web Game Backend
======================

This project is a Flask-based backend server for a web-based game. It features a simple player setup and management system, where each player is assigned a secret message and a unique session token.

Features
--------

-   Player Management: Add and remove players, each with a unique name, session token, and secret message.
-   Dynamic QR Code Generation: Each player gets a QR code linking to their personalized game page.
-   Player Page: Players can view their number, name, and secret message.
-   Simple Navigation: Easy navigation between setup and player pages.

Installation
------------

Before running the application, you need to install the required Python packages:

bashCopy code

`pip install Flask qrcode[pil]`

Running the Application
-----------------------

To start the server, run the following command in the project directory:

bashCopy code

`python app.py`

The server will start on `http://127.0.0.1:5000/`. You can access the setup page at `http://127.0.0.1:5000/setup`.

Usage
-----

-   Setup Page (`/setup`): Add new players by entering a name and clicking "Add Player". Each player will be assigned a random session token and a secret message. Players can be removed using the "Remove" link.
-   Player Page (`/player/<sessionToken>`): Players can view their details, including their assigned number, name, and secret message, by scanning their QR code or accessing their unique link.

Project Structure
-----------------

-   `app.py`: The main Python file with Flask routes.
-   `templates/`: Folder containing HTML templates for the web pages.
    -   `setup.html`: Template for the setup page.
    -   `player.html`: Template for the player page.

Dependencies
------------

-   Flask: A lightweight WSGI web application framework.
-   qrcode[pil]: QR Code image generation library.

License
-------

This project is open source and available under the MIT License.

* * * * *
