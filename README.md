| Simplify URL | <br>
(a URL shortener) <hr>

 BL Program <hr>

Details: <br>
This is a web application that takes in user inputted URL's and returns a shorter, simplified version of it. This was created using the Django web framework and SQLite as the backend database. <br><hr>

How it works (a simple summary): <br>
When a user submits a unique URL, a random string is crafted, and a shortened URL is created through the appendation of that string onto the domain. Both the user inputted URL and the simplified URL are added into the database. When the simplified URL is visited, the visitor is able to be redirected to the original URL because of that aforementioned database. <br><hr>

How to start (a guide):
For starters, you could visit the <a href="https://simplifyurl.pythonanywhere.com/">site</a> to try it out and see what it does. <br> <br>
Then: <br>
1. Download the repository and open the folder 'SimplifyURL-main' with an IDE of your choice. <br>
2. Create a virtual environment and activate it. From there, install the requirements in the requirements.txt file located in the shortURLProject directory with your shell; (pip install -r requirements.txt) <br>
3. Enter the project directory (SimplifyURL-main>shortURLProject) and make the necessary migrations. Make the migrations via command line with the command 'py manage.py makemigrations'. Then migrate those aforementioned migrations with the command 'py manage.py migrate' (windows-based).<br>
4. Again, while you are in the project directory (SimplifyURL-main>shortURLProject), create a .env file and input: SECRET_KEY= with a key of your choice.
5. Run the server locally with the command 'python manage.py runserver'. <br>
Feel free to make any adjustments based off of your requirements. <hr>

Currently working on: <br>
~Minor quality of life improvements <br>
~Preparing for deployment <br>
