# PoliTruthApp

> An API backend I created while learning RestAPI Driven Applications using Flask.
Create Users, Each user can create Add, Publish, Unpublish and Delete Politician
Users can add their own Image Cover and Image Covers of their politicians.


## All Routes:


### Create, register, and send confirmation Email to user

> /users

> /users/{username}

> /users/{username}/politicians

> /users/activate/{token}

> /users/avatar

## Return current user

> /me

### Login Tokens

> /token

> /refresh

> /revoke


### User create, publish, update, unpublish, delete, and add profile image to Politician

> /politicians

> /politicians/{id}

> /politicians/{id}/publish

> /politicians/{id}/cover

# Instructions 

> Clone the Repo. Create a Python VENV. Install requirements. Create MAILGUN account and configure Domain/API. Use Postman
to test the endpoings. 
