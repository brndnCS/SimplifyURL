from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from urllib.parse import urlparse
from .models import myURL
import random
import string
import re


#Home page view
def showIndexHTML(request):
    return render(request, 'myApplication/index.html')


#Generates a random string to use for our shortened URL
def getRandom(length=5) -> str:
    blockedWords = ['admin', 'simplify', 'custom', 'login']
    availableCharacters = string.ascii_letters + string.digits

    temp = ''.join(random.choices(availableCharacters, k=length))

    while myURL.objects.filter(simplifiedURL = temp).exists() and temp in blockedWords:
        temp = ''.join(random.choices(availableCharacters, k=length))
        
    return temp


#Cleans our URL. This reduces the entries in our database and limits each address to a maximum of 2 links (either with or without 'www').
#Originally, it added 'www' as the subdomain no matter what, but sites often have various subdomains
def cleanInput(string) -> str:
    parsedURL = urlparse(string)

    if not parsedURL.scheme:
        string = 'https://' + string
    
    if string[-1] == '/':
        string = string[:-1]

    return string


#Checks if a custom URL string is valid
def isValidString(string: str) -> bool:
    blockedWords = ['admin', 'simplify', 'custom', 'login']

    #Decided not to go with a profanity filter because of the infamous Scunthorpe problem
    if string in blockedWords:
        return False
    
    else:
        #only alphanumerics, underscores, and hyphens
        return bool(re.fullmatch(r'^[a-zA-Z0-9_-]+$', string))


#Backend logic for url shortening
def simplify(request):
    if request.method == 'POST':
        userInput = cleanInput(request.POST.get('userInput'))
        
        #Has this URL entered our database before?
        checkDatabaseURL = myURL.objects.filter(inputURL=userInput, isCustom=False).first()

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
            myURL.objects.create(inputURL = userInput, simplifiedURL = tempString, isCustom = False)
            return render(request, 'myApplication/index.html', {'simplifiedURL': simplifiedURL})

    else:
        #app_name : url_name
        #send back to home page if it's not a post req
        return redirect('myApplication:indexHTML')


#Backend logic for a custom alias for a URL
def customURL(request):
    if request.method == 'POST':
        #get the customURL that the user has inputted
        destinationURL = cleanInput(request.POST.get('destinationURL'))
        customUserInput = request.POST.get('customURL')
        
        if isValidString(customUserInput) == False:
            return render(request, 'myApplication/index.html', {'invalidString' : customUserInput})

        #check DB if a user has inputted a simplified URL that already exists
        checkDatabase = myURL.objects.filter(simplifiedURL=customUserInput).first()

        #conflict within the DB
        if checkDatabase is not None:

            customURL = request.build_absolute_uri('/') + customUserInput
            return render(request, 'myApplication/index.html', {'error' : customURL})
        
        #no conflict, add to database
        else:
            customURL = request.build_absolute_uri('/') + customUserInput
            myURL.objects.create(inputURL = destinationURL, simplifiedURL = customUserInput, isCustom = True)
            return render(request, 'myApplication/index.html', {'customURL' : customURL})

    #send back to home page if it's not a post req
    else:
        return redirect('myApplication:indexHTML')


#Redirection
def simplifyRedirect(request, simplifiedURL):
    #go through database and get our OG link
    inputURL = myURL.objects.get(simplifiedURL = simplifiedURL).inputURL
    
    #gets us back to the original destination a user has inputted
    return redirect(inputURL)