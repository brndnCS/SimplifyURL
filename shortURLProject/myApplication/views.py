from django.shortcuts import render
from django.shortcuts import redirect
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import myURL
import random
import string
import re


#Home page view
def showIndexHTML(request):
    return render(request, 'myApplication/index.html')


#Returns a random string to use for our shortened URL
def getRandom(length=5) -> str:
    blockedWords = ['admin', 'simplify', 'custom', 'login']
    availableCharacters = string.ascii_letters + string.digits

    temp = ''.join(random.choices(availableCharacters, k=length))

    while myURL.objects.filter(simplifiedURL = temp).exists() and temp in blockedWords:
        temp = ''.join(random.choices(availableCharacters, k=length))
        
    return temp


#Checks if a custom URL string is valid
#Returns true if it is; false if it's not
def isValidString(string: str) -> bool:
    blockedWords = ['admin', 'simplify', 'custom', 'login']

    #Decided not to go with a profanity filter because of the infamous Scunthorpe problem
    if string in blockedWords:
        return False
    
    else:
        #only alphanumerics, underscores, and hyphens
        return bool(re.fullmatch(r'^[a-zA-Z0-9_-]+$', string))


#Returns true if our URL is valid; Returns false is it isn't.
def validateURL(url):
    validator = URLValidator()
    try:
        validator(url)
        return True
    
    except ValidationError:
        return False


#Basic URL string parsing on top of input prereqs
#Returns a tuple in the format: [url string, conditional boolean]
#Conditional Boolean -> If it ever returns False, we can't proceed
def parsing(string):
    string = string.lower()

    if string[-1] == '/':
        string = string[:-1]
    
    tempParse = urlparse(string)

    conditional = True
    if tempParse.scheme != 'https' and tempParse.scheme != 'http':
        conditional = False

    if validateURL(string) == False:
        conditional = False

    if tempParse.netloc[0:4] == 'www.':
        string = tempParse.scheme + '://' + string[len(tempParse.scheme)+7:]

    return [string, conditional]


#Backend logic for url shortening
#Returns a simplified url if all conditions are met
def simplify(request):
    if request.method == 'POST':
        userInput = parsing(request.POST.get('userInput'))
        
        if userInput[1] == False:
            return render(request, 'myApplication/index.html', {'schemeIssue': userInput[0]})
        
        #Has this URL entered our database before?
        checkDatabaseURL = myURL.objects.filter(inputURL=userInput[0], isCustom=False).first()

        #Yes
        if checkDatabaseURL is not None:
            simplifiedURL = request.build_absolute_uri('/') + checkDatabaseURL.simplifiedURL
            return render(request, 'myApplication/index.html', {'simplifiedURL': simplifiedURL})
        
        #No
        else:
            tempString = getRandom()
            simplifiedURL = request.build_absolute_uri('/') + tempString

            #Add to database
            myURL.objects.create(inputURL = userInput[0], simplifiedURL = tempString, isCustom = False)
            return render(request, 'myApplication/index.html', {'simplifiedURL': simplifiedURL})

    else:
        #Reload back to index.html
        return redirect('myApplication:indexHTML')


#Backend logic for a custom alias as a URL
#Returns a custom url if all conditions are met
def customURL(request):
    if request.method == 'POST':
        destinationURL = parsing(request.POST.get('destinationURL'))
        customUserInput = request.POST.get('customURL')
        
        if destinationURL[1] == False:
            return render(request, 'myApplication/index.html', {'schemeIssue2': destinationURL[0]})

        if isValidString(customUserInput) == False:
            return render(request, 'myApplication/index.html', {'invalidString' : customUserInput})

        #Check for existence
        checkDatabase = myURL.objects.filter(simplifiedURL=customUserInput).first()

        #Conflict
        if checkDatabase is not None:
            customURL = 'filler'
            return render(request, 'myApplication/index.html', {'error' : customURL})
        
        #No conflict
        else:
            customURL = request.build_absolute_uri('/') + customUserInput
            myURL.objects.create(inputURL = destinationURL[0], simplifiedURL = customUserInput, isCustom = True)
            return render(request, 'myApplication/index.html', {'customURL' : customURL})

    #Restart
    else:
        return redirect('myApplication:indexHTML')


#Redirection to the original url
def simplifyRedirect(request, simplifiedURL):
    inputURL = myURL.objects.get(simplifiedURL = simplifiedURL).inputURL
    
    #Gets back to the original destination
    return redirect(inputURL)
