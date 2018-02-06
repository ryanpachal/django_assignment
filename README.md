To get the server running locally:

Clone repo:
  git clone https://github.com/ryanpachal/django_assignment.git

Create new virtual environmnet:
  virtualenv test
  source test/bin/activate
  
 Install all dependencies:
  pip3 install -r requirements.txt
  
 Create a new MySQL DB:
  mysql -u root -p
  (once logged into MySQL shell)
  CREATE DATABASE dashmd_django CHARACTER SET UTF8;
  CREATE USER dashmd_django@localhost IDENTIFIED BY 'password';
  GRANT ALL PRIVILEGES ON dashmd_django.* TO dashmd_django@localhost;
  FLUSH PRIVILEGES;
  exit
  
 Migrate DB:
  python manage.py migrate
  
 Populate DB with test data:
  python toronto_locations_into_db.py
  
 Run server:
  python manage.py runserver
  
 Try different queries such as:
  localhost:8000/rest_api/distances?latitude=43.654262&longitude=-79.385975&radius=1000&max_count=5
  localhost:8000/rest_api/distances?latitude=43.654262&longitude=-79.385975&radius=1000&max_count=5&Categroy=Library
  localhost:8000/rest_api/locations?name=Bendale
  
  
 
