| Simplify URL | <br>
(a URL shortener) <hr>

 BL Program <hr>

Details: <br>
This is a web application that takes in user inputted URL's and returns a shorter, simplified version of it. This was created using the Django web framework and SQLite as the backend database. <br><hr>

How it works (a simple summary): <br>
When a user submits a unique URL, a random string is crafted, and a shortened URL is created through the appendation of that string onto the domain. Both the user inputted URL and the simplified URL are added into the database. When the simplified URL is visited, the visitor is able to be redirected to the original URL because of that aforementioned database. <br><hr>

How to start (a guide):
For starters, you could visit _______ to try it out. <br> <br>
1. Download the repository and open the folder 'SimplifyURL-main' with the IDE of your choice. <br>
2. Create a virtual environment and install Django. <br>
3. Enter the project directory (SimplifyURL-main>shortURLProject). <br>
4. Make the migrations via command line with the command 'py manage.py makemigrations'. (windows) <br>
5. Migrate those aforementioned migrations with the command 'py manage.py migrate'. <br>
6. Run server with the command 'py manage.py runserver'. <br>
Feel free to make adjustments based off of your requirements. <hr>

Currently working on: <br>
~Minor quality of life improvements <br>
~Preparing for deployment <br>
