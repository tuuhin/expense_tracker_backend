# Expense Tracker Backend

### :small_red_triangle: About
This project is a rest-ful api made used `django-rest-framework` ,`django` and `python`. As the name suggest it's a api for tracking your expense data wia a mobile app made with `flutter` .Visit  [link]("https://github.com/tuuhin/expense_tracker") to head over to see the mobile app .
   
### :bookmark_tabs: Back-End
Being a `django ` project , using it's abilities to seperate the content into apps. We have created three apps :

- [x] base
- [x] api
- [x] plans 

#### :briefcase: base 
Base deals with the authentication and authorization stuff,for the authentication we have used `json web tokens` for more information  [jwt]("https://jwt.io) . There is a functionality to create profiles ,with images ,for storing the images `aws-s3` buckets are used. To see the available [routes]("https://github.com/tuuhin/expense_tracker_backend/blob/main/base/urls.py").


#### :flying_saucer: api
Api is related to most of the basic routes to deal with incomes and expenses.With the context of the project this is the main app, which deals with the most important job .Too see the [routes]("https://github.com/tuuhin/expense_tracker_backend/blob/main/api/urls.py")

#### :man_playing_handball: plans
This app is contains all of your planning with the amount of money that you track off. currently the only features available for this app is to add ***goals*** and to create ***budget***

### :anchor: DataBase
For every `backend` app `database` is one of the most important thing. The app is configured for `sqlite` database but other databases like  [postgres]("https://www.postgresql.org/") or [mysql]("https://www.mysql.com/") could be used .To use other database change `DATABASES` under `settings.py` in expense_tracker or `PROJECT_FOLDER` 
- configuration for ***postgress***
```bash
    pip install psycopg2
```
```py
DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': env('HOST'),
        'NAME': env('NAME'),
        'USER': env('USER'),
        'PASSWORD': env('PASSWORD'),
        'PORT': 5432,

    }

}
```
- configuration for ***mysql***
```bash
    pip install mysqlclient
```
```py
DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql',
        'NAME':env("NAME"),
        'USER':env("USER"),
        'PASSWORD':env('PASSWORD'),
        'HOST':env('PORT'),
        'PORT':'3306',   
    }

```

### :construction: To contribute

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
If you have included postgress or mysql configuration for the databases, include some more variables  in **.env.local** file.
```
# postgressor mysql

HOST=
NAME=
USER=
PASSWORD=
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
This is  🧱 finished for the mean time ,all the routes are checked ,further development of the project would occur if the front end demands.
