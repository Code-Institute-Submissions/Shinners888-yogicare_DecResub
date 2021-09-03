# MS4 Full Stack Development Project

[Yogicare](https://yogicare.herokuapp.com/) is a Yoga Studio specialising in expecting and/or young families to guide early developmental health and well being. Visitors can log in to purchase online classes specific to theirs and their childs' needs. There is also a store to buy yoga accessories.


## UX

### User Stories:
Visitor
- I want to be able to view the site on any device.
- I want to be able to register to the site.
- I want to be able to view available class and shop prices.
- I want to have the ability to see the social media for the business

Registered User:
- I want to be able to log in/out with my registered details.
- I want to be able to view my Cart and any items I currently have awaiting payment in my Cart.
- I want to be able to add edit and remove items from my cart.

Application Owner/Administrator User:
- I want easy login to manage the site
- I want to have the ability to edit add and delete new classes and shop items
- I want to be able to view orders

### Visual
The colour scheme is cream and charcoal. These are calm but well-contrasted colours. There is a cream transparent overlay over a background image covering 100% viewheight. The background image changes for small devices.

The background image disappears for the checkout/checkout-success pages.

The font throughout the site is Montserrat.


# Technologies Used

- HTML, CSS, JS & Python - Languages
- Django - Project Framework framework.
- [Bootstrap](https://getbootstrap.com/) CSS Framework, JQuery and JS
- [Github](https://github.com/) (Gitpod) - Repository and development/version control
- [Heroku] - To deploy application
- - Postgres via Heroku
- [PEP 8 Online Validator](http://pep8online.com/)
- [W3C Schools Validators](https://validator.w3.org/nu/)
- [Stripe](https://www.stripe.com/)
- [Amazon Web Services](https://aws.amazon.com/console/)
---
- [Font Awesome](https://fontawesome.com/)
- [Favicon.ico](https://www.favicon.cc/)
- [Unsplash](https://unsplash.com/)
- [Stocksnap.io](https://stocksnap.io/)

# Creation and Bugs

This site is modelled on the Boutique Ado Walkthrough site. 

Apps:
- Home
- Profiles
- Shop
- Bag
- Checkout



Due to significant bugs in the development process, the 'classes' app had to be removed at deployment.
Remaining bugs include:
- Colours vs items in bag. Items with colour options are not functionally specified in the cart.
- Subtotal and quantity not displaying properly in bag template or successful checkout template.
- Search bar not working outside development environment.

While some bugs were fixed in time, in particular, migration issues with the Postgres Database and webhook handler issues, many still would not work and were cuasing sitewide bugs.

Future updates to include:
Classes and categories of classes. 
A review section in each class only to be modified by people who have purchased that class.
Fixing the items_by_colour bug
Fixing the search bug.
Fixing the order total/subtotal bug.


# Deployment

The project was developed in Gitpod and the app deployed to Heroku as outlined below:

Create new app in Heroku with local region setting. In resources, add Heroku Postgres to manage the databases.

Connect app to the github repository in the deploy tab.

In Settings, open Reveal Config Vars and set the following values:
- 'AWS_ACCESS_KEY_ID' : 'key_here'
- 'AWS_SECRET_ACCESS_KEY' : 'key_here'
- 'DISABLE_COLLECTSTATIC' : '1' <!--this will be deleted later->
- 'EMAIL_HOST_PASS' : 'key_here'
- 'EMAIL_HOST_USER' : 'key_here'
- 'SECRET_KEY' : 'key_here'
- 'STRIPE_PUBLIC_KEY' : 'key_here'
- 'STRIPE_SECRET_KEY' : 'key_here'
- 'STRIPE_WH_SECRET' : 'key_here'
- 'USE_AWS' : 'boolean_key_here'

In the gitpod console, install: gunicorn, psycopg and dj_database_url. Freeze to requirements.txt.

Creat a Procfile with `web: gunicorn yogicare.wsgi:application`

Log in to Heroku via the console. Before deploying, migrations need to be run again. I did not have fixtures in this project, but if you are using fixtures, this is the time to load them to the Postgres database. You will need to create the superuser again here.

In the Deploy tab, under Deployment method, selected GitHub and then set up automatic deploys. When the app has finished building, click Open app button on the top right of the page. This creates the app for git to push to.

- `python3 manage.py makemigrations --dry-run`
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- `python3 manage.py loaddata 'file-name'`
- `python3 manage.py createsuperuser`
Follow the prompts.
 

In settings.py, import dj_database_url, then the Databases section is updated to include an if-else statement regarding the postgres database url in Heroku:

`if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
            }`

Update Settings.py with `ALLOWED_HOSTS = ['yogicare.herokuapp.com', 'localhost']`
Add Stripe environment variables to settings.py.

- STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
- STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
- STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

These keys will be read from the Heroku config variables.
Push to Heroku using the following command: `git push heroku main`

If you get an operational error in your app, run `unset PGHOSTADDR` in your gitpod terminal.

The final step when the project is complete is to ensure development is set to false in settings.

## AWS Bucket Setup

The media and static files for this project are stored, like the Boutique Ado, in Amazon Web Services.

In the terminal, `pip3 install boto3` and `django-storages`

Log into your AWS account or create new. Follow [these](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) stepsto set up the bucket. 

Add storages to settings.py in your project.

Configure a new bucket with the correct permissions and CORS configuration.

Set up a group related to your project, with a User in the group. 

Return to the app bucket, inside, create a folder called media. Upload all project images here.

In settings.py 
'if 'USE_AWS' in os.environ:

    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }

    AWS_STORAGE_BUCKET_NAME = 'yogicare'
    AWS_S3_REGION_NAME = 'eu-west-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Static and media files
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
'
In Heroku, remove DISABLE_COLLECTSTATIC as a variable. 

Add commit and push project from Gitpod (or your IDE). The app should now have the static files and media available on the web service.
## Media and Credits

Images from [Unsplash](https://unsplash.com/) and [Stocksnap.io](https://stocksnap.io/)
  
[Image Missing](https://icon-library.com/icon/no-picture-available-icon-1.html)

This projected is modelled on the Boutique Ado Walkthrough Project. 

[Simple is better than complex](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html) helped with faulty migrations and errors with models in the deployed project.

The Slack and [Stack Overflow](https://stackoverflow.com/) communities 

# Acknowledgments
I would like to offer a sincere thank you to my mentor Nishant for his continued patience, encouragement and support.