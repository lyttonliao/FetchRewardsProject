## Installation


Cloning the project:
```
git clone https://github.com/lyttonliao/FetchRewardsProject.git
```

Downloading Python and creating a virtual environment to isolate package 
dependencies:
```
brew install python
python3 -m venv env
source env/bin/activate
```

Install Django and Django REST framework:
```
pip3 install django
pip3 install djangorestframework
```

Getting the project started:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```


## Testing the API


To run the unit tests that covers the example provided in the document:
```
python3 manage.py test transactions
```

To test the API locally, please visit (http://127.0.0.1:8000)! To start off, 
let's create a new user to gain and spend some points.

request URL: (http://127.0.0.1:8000/users/)  
request method: POST  
![Create user](https://github.com/lyttonliao/FetchRewardsProject/blob/main/assets/fetch_ss1.png)
Enter any username you'd like, and points will default to 0; then click POST
on the bottom right.

Next up, create our three payers in this specific order: Dannon, Unilever, 
and Miller Coors. This is done in the same way as users.  
request URL: (http://127.0.0.1:8000/payers/)  
request method: POST  

For the final steps of the project, we will be adding the transactions to that
user from the three payers we just created. We have to enter these sorted by
their timestamps in order for the transactions with negative values to deduct
points from the earliest positive transactions.

request URL: (http://127.0.0.1:8000/transactions/)  
request method: POST  
When adding these into the in-built django form, there are two ways to enter 
paramters: either copy the below dictionaries as raw data or the HTML form in 
which you can select the user and payer from dropdown menus with their string
representations, and manually enter points and the timestamp.
![Create payers](https://github.com/lyttonliao/FetchRewardsProject/blob/main/assets/fetch_ss2.png)

```
{ "user": 1, "payer": 1, "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
{ "user": 1, "payer": 2, "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
{ "user": 1, "payer": 1, "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
{ "user": 1, "payer": 3, "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
{ "user": 1, "payer": 1, "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
```

If you head back to (http://127.0.0.1:8000/users/), then you can check that
the user with id = 2, has a total of 11300 points.

To spend a users points, we will send a patch request to a specific user route:
request URL: (http://127.0.0.1:8000/users/<pk>/)  
request method: PATCH  

In my case, pk = 2. Important! You must select "Raw Data" and enter the 
following, then press PATCH.
```
{"points": 5000}
```

![Spend user points](https://github.com/lyttonliao/FetchRewardsProject/blob/main/assets/fetch_ss4.png)  

Should now look like this! This is the response to the spend call:  

![Show spend call response](https://github.com/lyttonliao/FetchRewardsProject/blob/main/assets/fetch_ss5.png)  

Last but not least, the final call to the points balance route:  

![Point balance call](https://github.com/lyttonliao/FetchRewardsProject/blob/main/assets/fetch_ss6.png)  