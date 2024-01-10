# Cyber Security Base 2023: project 1
### This is a project with 5 cyber security flaws from OWASP top ten list from 2017, including CSRF-vulnerability flaw.

Some software design choices were made with the help of material of the cyber security base 2023 course, especially with the help of a programming exercise "CSRF Prompt-By Pass".

## To start the application:
- $ python3 manage.py runserver
- go to: localhost:8000/
- log-in credenntials are as in the programming exercises, bob:squarepants and alice:redqueen
## FLAW 1: Injection 
https://github.com/maxxof/csb-project-1/blob/b50b06289714e52d0d44f4ed05ef4e4b7ca8654b/server/pages/views.py#L37C1-L37C1 
 
DESCRIPTION: 

This flaw predisposes a system to many SQL-injections via HTML-form making it possible for the attacker to modify software’s database by inserting abnormal code in the form’s text box. This flaw includes updating a database with unparameterized SQL’s UPDATE query, in which new account balance is calculated in previous try-except block by supposing that a transfer amount is given as an integer. If form data contains anything other than integer program skips that block and jumps straight to making a query. That way form data is no filtered so it becomes directly a part of the UPDATE query. In that scenario it is possible to insert an comment characters (“--”) so the latter part of the query doesn’t get executed. One possible injection in our software would be inserting string “0; --” (without quotations) that would reset every user’s account balance to zero. This is also a sub-flaw of Broken Access Control-flaw since an entity can modify other users account balances. 

FIX: 


https://github.com/maxxof/csb-project-1/blob/b50b06289714e52d0d44f4ed05ef4e4b7ca8654b/server/pages/views.py#L43C15-L43C15 
Easiest an most reasonable fix would be to user Django’s in-built object system for database operations as it was used in previous try-except block. Also fixing the try-except block to only accept integers would fix the issue. If for some reason it is not wanted to use Django’s objects the fix would be to change the query to parameterized query provided as a comment. 

 
## FLAW 2: Broken Access Control 
https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/server/pages/views.py#L21 

DESCRIPTION:

This flaw predisposes a system to unauthorized access to other users account balance by poor authorization system and system architecture, which is based on form using GET-method instead of POST-method. This vulnerability gives an user possibility to transfer money from any user’s account to desired account simply by putting right parameters (such as /transfer/?from=bob&to=alice&amount=9999) into the url. Program does not have any authorization system since all the transfer logic is based on GET-parameters given in the HTML-form. The biggest and most concerning design flaw here is extracting sender’s information from a form, which instead should be configured in the backend using built-in tools such as request.user. This flaw gives a direct possibility for CSRF-attacks which will be presented next. 

FIX: 

https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/server/pages/views.py#L12 
First step would be changing the form method from GET to POST. Then we add a check that a request uses truly “POST” method. Next we extract the receiver with request.POST.get() method and for the correct authorization we extract sender as a user of the request, making it impossible to set a different sender. 

 
## FLAW 3: CSRF-vulnerability 
https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/server/pages/views.py#L21C50-L21C50 

DESCRIPTION: 

CSRF-vulnerability flaw of our system is linked to previously presented broken access control, with few extra modifications. This flaw makes it possible for authenticated users to transfer money without their authorizations, by, for example, opening an file which automatically makes an request to the server which will transfer money from victim’s account to desired account. This can be demonstrated with the file csrf.html in the directory csrf_vulnerability by running a new server and opening a file on it while being logged in on the base server. 
https://github.com/maxxof/csb-project-1/blob/main/csrf_vulnerability/csrf.html 

FIX: 

https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/server/pages/views.py#L14 
Fix for this vulnerability is almost the same as it is for the broken access control flaw, but by adding csrf-tokens to each request and checking that the request has wanted ‘csrfmiddlewaretoken’. This way previous phishing method with csrf-file won’t work since it no longer uses a GET-method and the sender is extracted as an authenticated request user. 

 
## FLAW 4: Sensitive Data Exposure 
https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/server/pages/views.py#L66C2-L66C2 

DESCRIPTION: 

This software security flaw can expose users sensitive data to unauthorized users. The flaw is similar to broken access control since it is a product of a poor software design choice by using parameterized GET-method. If an user logged in it can gain access to other users accounts balance simply by inserting an username into the url (for example typing /balance/alice as a bob can view alice’s balance). Account balance is a sensitive information, just as the passwords are, in every banking system and it shouldn’t be available to other users. 
 
FIX: 

https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/server/pages/views.py#L60 
Fix for the issue is straightforward – extracting the user information in the backend from a request, making it once again impossible to change. Although this change fixes the problem, from a software design and UX standpoint it would make sense to display the balance in the index.html without routing to another HTML-template. 
 
 
## FLAW 5: Using Components with Known Vulnerabilites 
https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/requirements.txt#L10 
And 
https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/requirements.txt#L19 

DESCRIPTION: 

Django’s most recent vulnerable version (4.2.3) has some vulnerabilities linked to denial of service. Second dependency with known vulnerabiltiy is restview and it’s version 2.8.0 which has issues regarding HTTP requests. 

FIX: 


https://github.com/maxxof/csb-project-1/blob/9a857b779b62baa232f8c323d39db6b74c3fa8d9/requirements.txt#L9C26-L9C26 
Easy fix is to download the latest versions of django and restview that has fixes for previous issues. 
