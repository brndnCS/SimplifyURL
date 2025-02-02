from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import myURL
import random
import string

#home page view
def showIndexHTML(request):
    return render(request, 'myApplication/index.html')

#Generates a random string to use for our shortened URL
def getRandom(length=8):
    availableCharacters = string.ascii_letters + string.digits
    
    for idx in range(5):
        temp = ''.join(random.choice(availableCharacters))
    
    while myURL.objects.filter(simplifiedURL = temp).exists():
        temp = ''.join(random.choice(availableCharacters))
    
    return temp

#user inputs a valid url and clicks the 'simplify' button
def simplify(request):
    if request.method == 'POST':
        #refer to index.html for name of the search-bar
        userInput = request.POST.get('userInput')
        
        #Has this URL entered our database before?
        checkDatabaseURL = myURL.objects.filter(inputURL=userInput).first()

        #Yes
        if checkDatabaseURL is not None:
            #get the absolute url with django's method
            simplifiedURL = request.build_absolute_uri('/') + checkDatabaseURL.simplifiedURL
            return render(request, 'myApplication/index.html', {'simplifiedURL': simplifiedURL})
        
        #No
        else:
            tempString = getRandom()
            simplifiedURL = request.build_absolute_uri('/') + tempString

            #add user's URL to the database; along with the simplified version
            myURL.objects.create(inputURL = userInput, simplifiedURL = tempString)
            return render(request, 'myApplication/index.html', {'simplifiedURL': simplifiedURL})

    else:
        return HttpResponse("Error 1")

def simplifyRedirect(request, simplifiedURL):
    #go through database and get our OG link
    inputURL = myURL.objects.get(simplifiedURL = simplifiedURL).inputURL
    
    #gets us back to the original destination a user has inputted
    return redirect(inputURL)
