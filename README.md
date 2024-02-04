Amazon Price Comparison:
This project is a web application that allows users to search for products on Amazon and compare their prices across different Amazon marketplaces (US, UK, Germany, and Canada). Users can also view their past searches. The application features bonus functionalities like a reset option and a responsive design that adapts to different screen sizes and devices.

Table of Contents:
-Installation
-Usage
-File Structure
-Functionality
-Installation

Prerequisites:
-Python 3.8 or higher
-Flask
-Steps

Clone the repository to your local machine.
Install the required dependencies by running pip install -r requirements.txt in the project folder.
Run the application using flask run or python app.py.
-Usage
Open the web application in your browser (default address is http://127.0.0.1:5000/).
Enter a product name in the search bar and click "Search."
The application will display a list of matching products.
Click on a product to view its price in different Amazon marketplaces.
Click on the "Past Searches" button to view a list of your previous searches.
Click on the "Reset" button to reset the daily search count.

-File Structure
app.py: The main Flask application file.
database.py: A Python file containing functions to interact with the SQLite database.
requirements.txt: A file listing the required Python packages for this project.
static/js/main.js: JavaScript file containing client-side logic.
templates/index.html: The main HTML template for the web application.

-Functionality
*Search
Enter a product name to search for products and compare their prices across different Amazon marketplaces.

Past Searches
View a list of past searches by clicking the "Past Searches" button.


*Responsive Design
The application has a responsive design that adapts to different screen sizes and devices.