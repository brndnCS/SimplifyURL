| SimplifyURL | <br>
(a URL shortening service) <hr>
BL Program <hr>
https://simplifyurl.pythonanywhere.com/ <hr>

Project Details: <br>
Full stack web application that requests a user to input a URL of their choice, and returns a shortened version of that same URL. This was created using Python, HTML + CSS, the Django web framework, a web hosting service (PythonAnywhere), and a SQLite database for URL storage. <br><hr>

How it works (a simple summary): <br>
When a user submits a unique URL, a random string is crafted, and a shortened URL is created through the appendation of that random string onto the domain. Both the user inputted URL and the simplified URL are added into the database. When the simplified URL is visited, the visitor is redirected to the original URL linked within the aforementioned SQLite database. <br><hr>

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
~<s>Preparing for deployment </s><br>
~<s>UI improvements </s><br>
~<s>An option to use a custom link rather than a randomly generated one </s><br>
~<s>Minor quality of life improvements </s><br>
~<s>A copy to clipboard button </s><br>
