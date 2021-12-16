# MS4 Full Stack Development Project

[Yogicare](https://yogicare.herokuapp.com/) is a Yoga Studio specialising in expecting and/or young families to guide early developmental health and well being. Visitors can log in to purchase online classes specific to theirs and their childs' needs. There is also a store to buy yoga accessories.


## UX

### User Stories:
Visitor
- I want to be able to view the site on any device.
- I want to be able to register to the site to save details for a faster checkout.
- I want to be able to view and purchase available items as a guest.
- I want to have the ability to see the social media for the business

Registered User:
- I want to be able to log in/out with my registered details.
- I want to be able to view my Cart and any items I currently have awaiting payment in my Cart.
- I want to be able to add edit and remove items from my cart.

Application Owner/Administrator User:
- I want easy login to manage the site
- I want to have the ability to edit add and delete new items
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

This site is modelled on the Boutique Ado Walkthrough site. In particular throughout the views, models and layout. 

Apps:
- Home
- Profiles
- Shop
- Bag
- Checkout


Due to significant bugs in the development process, the 'classes' app had to be removed at deployment.
Remaining bugs include:
- Colours vs items in bag. Items with colour options are not functionally specified in the cart. - Solved
- Subtotal and quantity not displaying properly in bag template or successful checkout template. - Solved
- Search bar not working outside development environment. - Removed

- An unnoted bug in the last submission of the project was that upon payment in the deployed app, the app was returning an error 500. At first this appeared to be a browser issue as not everyone was experiencing the issue, and the issue did not happen in the development version. Various issues played a role in this. I had failed to note that one of my webhooks was failing. This was partially due to the fact that the checkout successful emails were not set up. This fixed the issue with the development webhook. This did not seem to impact the deployed version though. Upon further inspection, it appeared to be a migration issue. A change made after my initial Postgres migration had not been migrated over. 

- This updated migration raised a new issue as it impacted the existing database in the Heroku app. Issues included the superuser not being able to delete items from the shop, users from the store, orders in the django Admin site, etc. Edits could be made, but nothing could be deleted and the delete button in the site threw a 500 error. The Postgres Database had to be reset and all Heroku migrations done again from scratch. This resolved this issue.

- After much searching, the problem with the totals not populating in the checkout success page (nor the admin orders section) turned out to be both a signals issue, and conflicting data types in line 52 of models.py. Upon adding `weak=False` to the signals, and updating the apps.py to import the signals. In checkout/models.py, the self.order_total was converted to a float to fix the conflicting data types issue.

- Adjusting the quantity of an item with colour options in the bag was causing an error. This I was unable to fix in time, so the quntity adjust function was removed from the bag. The Delete button remains. The obvious issue here is that if a user wants to reduce the amount of an item, they will have to delete and return to shop. This is currently better than the colour selections disappearing with any bag adjustments though and I felt it best to redo the bag this way.

While some bugs were fixed in time, in particular, migration issues with the Postgres Database and webhook handler issues, many still would not work and were causing sitewide bugs. As such, many of the user stories I wished to manage have not been successful.

## Testing

- The visitor lands on the home page. They can browse the website as an unregistered user and avail of the products offered. They can make a purchase as a guest but will not have an account with the company for faster use of the website in future.

- The navbar provides easy movement through the site. The visitor can navigate to the shop page where they will find items for sale. They can click on items of interest and add to cart. Some items have colour options. These are in a dropdown menu that the user can choose from. Once all items needed are in the bag, the user can navigate to their cart in the top right of the navbar. Once in the cart, there are bugs. If multiple colours of an item are in the cart, adjusting any of these results in other colours being eliminated completely.

- Otherwise, the user has the option of navigating to the checkout and purchasing as a guest. There is an option to register/login to save information on the site. The user will be required to use their email to purchase and will receive a confirmation email once the order is complete. To test this, I used the number 4242 4242 4242 4242 with any future date and any 5 digit number for the card details.

- They user will receive their order confirmation within the site straight away, with the order number for reference.

---
- To register to the site, you need an email address, a username and a password. Once entered, you will receive an email to your provided email address with a link to verify your details. This may take a few minutes, but then you are a verified user. You can view previous purchases and check out faster.

---
- As admin, you have the added option of adding, editing and deleting items from the store. On th eshop page, an option to add a new item will be under the heading. You can enter all required details about new products which will then display in the shop for all users. 

- To edit or delete an existing item, click on the item, and the edit/delete buttons will be below the item name.

- The bag and checkout bugs exist for all site users. It is still possible to make your purchase, and the items will show up perfectly in the order summary, provided no adjustments have been made to items of varied colours within the bag app. The admin will be able to see this too.


## Future updates to include:
Classes and categories of classes. 
A review section in each class only to be modified by people who have purchased that class.
Making adjustments for a more seamless user experience on smaller and mid size screens


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
`if 'USE_AWS' in os.environ:

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
`
In Heroku, remove DISABLE_COLLECTSTATIC as a variable. 

Add commit and push project from Gitpod (or your IDE). The app should now have the static files and media available on the web service.

## Cloning the repository

- Go to the [Repository](https://github.com/Shinners888/yogicare).

- Click the green button located above the files.

- Click the "clipboard icon" to the right of the Git URL to get the clone URL.

- Open your IDE terminal window.

- Change the directory to where you want to clone the repository.

- Paste the URL and click OK

- In the terminal type `pip install -r requirements.txt`

- Create an env.py file (or set environment variables if preferred), with the settings to match the config vars above. For development, make the required changes to settings.py, set debug to True and DATABASES to:

`DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
    }`
Remember to send env.py to .gitignore to keep sensitive information private.


## Media and Credits

Images from [Unsplash](https://unsplash.com/) and [Stocksnap.io](https://stocksnap.io/)
  
[Image Missing](https://icon-library.com/icon/no-picture-available-icon-1.html)

This projected is modelled on the Boutique Ado Walkthrough Project. 

[Simple is better than complex](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html) helped with faulty migrations and errors with models in the deployed project.

The Slack and [Stack Overflow](https://stackoverflow.com/) communities 

# Acknowledgments
I would like to offer a sincere thank you to my mentor Nishant for his continued patience, encouragement and support.