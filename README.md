# Expense Tracker Backend

### :small_red_triangle: About
This project is a rest-ful api made used `django-rest-framework` ,`django` and `python`. As the name suggest it's a api for tracking your expense data wia a mobile app made with `flutter` .Visit  [link]("https://github.com/tuuhin/expense_tracker") to head over to see the mobile app .
   
### :bookmark_tabs: Back-End
Being a `django ` project , using it's abilities to seperate the content into apps. We have created three apps :

- base
- api
- plans 

#### :briefcase: base 
Base deals with the authentication and authorization stuff,for the authentication we have used `json web tokens` for more information  [jwt]("https://jwt.io) . There is a functionality to create profiles ,with images ,for storing the images `aws-s3` buckets are used. To see the available [routes]("https://github.com/tuuhin/expense_tracker_backend/blob/main/base/urls.py").


#### :flying_saucer: api
Api is related to most of the basic routes to deal with incomes and expenses.With the context of the project this is the main app, which deals with the most important job .Too see the [routes]("https://github.com/tuuhin/expense_tracker_backend/blob/main/api/urls.py")

#### :man_playing_handball: plans
This app is currently in construction , most probably this app will contain the extra features realted to the app. Like adding `Goals` and `Savings` and others 

### :anchor: DataBase
For every `backend` app `database` is one of the most important thing. As the app is still under contruction so currenlty it's powered by `sqlite` database . After it's conplete most probably there will be a [postgres]("https://www.postgresql.org/") or [mysql]("https://www.mysql.com/") database.

### :construction: Contribute

Clone this repository 🔂
```bash
    git clone https://github.com/tuuhin/expense_tracker.git
    cd expense_tracker
```
This project requires a `.env.local` file which is referenced in `settings.py` file .

**Structure of the .env.local file**
```
# django only

SECRET_KEY=
DEBUG=

#aws
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
AWS_S3_SIGNATURE_VERSION=s3v4

#jwt
ACCESS_TOKEN_LIFETIME=
REFRESH_TOKEN_LIFETIME=
```
Fill the data as required to use this project,then

```bash
    pip install -r requirements.txt
```
To get the requirements for these project. It's adviced to use this project over a `virtualenv` or `venv`.

```bash
    python manage.py migrate
```
To apply all the migrations 

```bash
    python manage.py runserver 
```
To run the server

### :fortune_cookie: Conclusion
This is still under contruction.
