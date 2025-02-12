from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from urllib.parse import urlparse, urlunparse
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


#Cleans our URL. This reduces the entries in our database and limits each address to a maximum of 1 link (unless the website has various subdomains).
def cleanInput(string) -> str:
    string = string.lower()
    parsedURL = urlparse(string)

    if not parsedURL.scheme:
        string = 'https://' + string
    
    parsedURL = urlparse(string)
    netloc = parsedURL.netloc

    if parsedURL.netloc[0:4] == 'www.':
        netloc = netloc[4:]
    
    #Rebuild URL
    retString = parsedURL[0] + '://' + netloc + parsedURL.path + parsedURL.params + parsedURL.query + parsedURL.fragment
    
    if retString[-1] == '/':
        retString = retString[:-1]

    return retString


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
            simplifiedURL = request.build_absolute_uri('/') + checkDatabaseURL.simplifiedURL
            return render(request, 'myApplication/index.html', {'simplifiedURL': simplifiedURL})
        
        #No
        else:
            tempString = getRandom()
            simplifiedURL = request.build_absolute_uri('/') + tempString

            #Add to database
            myURL.objects.create(inputURL = userInput, simplifiedURL = tempString, isCustom = False)
            return render(request, 'myApplication/index.html', {'simplifiedURL': simplifiedURL})

    else:
        #Reload back to index.html
        return redirect('myApplication:indexHTML')


#Backend logic for a custom alias as a URL
def customURL(request):
    if request.method == 'POST':
        destinationURL = cleanInput(request.POST.get('destinationURL'))
        customUserInput = request.POST.get('customURL')
        
        if isValidString(customUserInput) == False:
            return render(request, 'myApplication/index.html', {'invalidString' : customUserInput})

        #Check for existence
        checkDatabase = myURL.objects.filter(simplifiedURL=customUserInput).first()

        #Conflict
        if checkDatabase is not None:
            customURL = request.build_absolute_uri('/') + customUserInput
            return render(request, 'myApplication/index.html', {'error' : customURL})
        
        #No conflict
        else:
            customURL = request.build_absolute_uri('/') + customUserInput
            myURL.objects.create(inputURL = destinationURL, simplifiedURL = customUserInput, isCustom = True)
            return render(request, 'myApplication/index.html', {'customURL' : customURL})

    #Restart
    else:
        return redirect('myApplication:indexHTML')


#Redirection
def simplifyRedirect(request, simplifiedURL):
    inputURL = myURL.objects.get(simplifiedURL = simplifiedURL).inputURL
    
    #Gets back to the original destination
    return redirect(inputURL)
