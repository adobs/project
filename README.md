![alt text](/static/img/okc_logo.png “Thanks to Leslie Castellanos for designing the logo”)

***

# Project Description

Ever heard of the dating site [OkCupid](https://www.okcupid.com/)? OKC+ takes OkCupid to the next level with innovative analytics and tools. The OKC+ database contains 58K profiles that were scraped from OkCupid. Users can explore the most commonly used adjectives from these profiles on a map, and filter results by 22 genders, 12 orientations, and an 80+ year age range. Alternatively, users can discover how different portions of people's profiles cluster based on machine learning using a mean shift clustering algorithm, displayed with interactive D3 and Chart.js visuals. Users can create an OkCupid account on the app, or login with their existing OkCupid credentials to access additional features, such as a messaging bot and a profile generator that uses Markov Chains.


# About the Logo

I created an OkCupid account.  I then analyzed **58K profiles** across the country of people that are interested in the group I fall into:

straight woman aged 18-36 years old.

This site shows you the profiles that I, *as a woman*, found.


# Table of Contents(unformatted list with links that jump to the section)

* [Setup](#setup)

* [Usage](#usage)

* [Tech Stack](#techstack)

* [APIs Used](#api)

* [About the Developer](#developer)



# <a name=“setup”></a>Setup

### Dependencies and Compatibility

* OSX.  Compatible as-is. 

* Linux.  Install dependencies using commands below

[sudo apt get from email, as code links]

* Windows.  Not compatible.  *Feel free to install a supported virtual machine with a supported environment in order to access OKC+.  Example: [VirtualBox](https://www.virtualbox.org/wiki/Downloads).*


### Installation

* Suggestion: create a virtual environment for the project  ```$ virtualenv env```.

* Activate the environment ```$ source env/bin/activate```.


### Install requirements ```$ pip install -r requirements.txt```

* From the command line of the terminal, run ```$ python flask_app.py```.

* In a browser window, type localhost:5000 to access the home page

* You are ready to party if you see the following: 
![Home Page](/static/gif/home.gif)


### Data

I used PostgreSQL to store the 58K profiles that I scraped.  I did not put my database on Github, so in order to access meaningful analytics, you will need to pull your own data after you have created an OkCupid account, and populate your own database.  Create your own PostgreSQL database called profiles_final by typing ```$ createdb profiles_final```.  Run the model.py file to create all the tables in the database with ```$ python model.py```.  


Add zipcodes to the Zipcodes table of locations you would like to search.  Then edit the file seeding_profile_database.py and enter in your own OkCupid username and password where the code currently says ```python session = Session.login('username', 'password')```. To begin populating the database, run ```$ python seeding_profile_database.py```.  After you are done, populate the remaining tables by running the following programs:

```$ python querying_the_data.py```
```$ python seed_adjective_table.py```
```$ python seed_location_table.py```
```$ python seed_person_gender_table.py```
```$ python seed_person_orientation_table.py```


Of note, the analytics you will see will be catered to the profiles you pull down.  This is determined by your self-selected demographic information (gender, orientation, age).  


# <a name=“usage”></a>Usage

### Account creation 
Create an account on OKC+.  Through use of Selenium[link], creating an account on OKC+ also simultaneously registers the account with OkCupid.


### Login
Login to OKC+ using OkCupid credentials to access all the features of the site


### OKCBot: Messaging Bot 
Fill out the form to send messages from your account to as many people on OkCupid that you would like.


### OKCBot: Profile Generator 
Fill out the form to generate a self-summary for your profile using Markov Chains, and click “Generate” when done.  A self-summary will populate, and then click on the button “Add to 'Self Summary' in my profile” to change your OkCupid profile to the generated text.


### Analytics: Adjective Map 
Based on the profiles in the database, this Google Maps map [link] will display the most common adjective used in people's self-summary per location. Filter by orientations, genders, and age, then click “Submit.”  Click on the marker for each location to open an info window that allows you to message OkCupid users that match your search in that location.

![Adjective Map](/static/gif/adjective_map_limited.gif)


### Analytics: Sankey Profile 
Based on the profiles in the database, a D3 Sankey Chart will display the results of a Scikit-Learn Mean Shift clustering algorithm.  The clustering algorithm clusters profiles based on the words used in the “Self-Summary” portion of the profile, and also clusters profiles based on the words used in the “Message Me If” section of the profile.  On hover, the words used to form the clusters appears, as well as a breakdown of demographics for each cluster using Chart.js.

![Sankey Profile](/static/gif/sankey_profile_limited.gif)


# <a name=“techstack"></a>Tech Stack

* Scikit-Learn 
* D3 
* Chart.js
* Selenium 
* NLTK 
* PostgreSQL 
* SQLAlchemy
* Python
* Numpy 
* Flask
* AJAX
* Javascript 
* jQuery 
* Pickle 
* Jinja 
* Geocoder 
* HTML 
* CSS
* Bootstrap


# <a name=“api”></a>APIs Used 

* [Okcupyd](http://okcupyd.readthedocs.org/en/latest/#)
* [Google Maps](https://developers.google.com/maps/?hl=en)


# <a name=“developer”></a>Developer

Alexandra Dobkin aka Dobs lives in San Francisco, CA.  Check out her professional life on [LinkedIn](https://www.linkedin.com/in/alexandradobkin).  Check out her personal life on [OkCupid](http://www-tc.pbs.org/prod-media/newshour/photos/2013/11/20/cat_meme_blog_main_horizontal.jpg).