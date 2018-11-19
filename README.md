# MyFavShows App <img src="./myfavshows/static/tvshow.png" alt="drawing" width="50" align="center"/>



## Collaborative school project

MyFavShows App enables any user to search for TV Shows. 
Registered users can add TV Shows to their favourites in order to get more details on the show such as the episodes' description.
They also can enable notifications whenever a new episode of one of their favourites is aired.

We dockerized the project and deployed it on Heroku, feel free to go check it out at <a href='https://myfavshows.herokuapp.com'> this address <a/>.

## Installation
1. Install the Python `virtualenv` package: 

	`pip install virtualenv`


2. Download the projet directory. Once the files unzipped/downloaded, create a python virtual environment in the said directory: 

	`cd /project_directory`
	
	`virtualenv venv`
	
	Linux / MacOS: `source venv/bin/activate`
	
	Windows: `.\venv\Scripts\activate.bat`


3. From the same directory, install the app and its dependencies:

	`pip install -e myfavshows/`
  
  
## Running the MyFavShows
   
1. Go to your virtualenv. Add the app to your environment variables:

	Linux / MacOS:`export FLASK_APP=myfavshows`
	
	Windows: `set FLASK_APP=myfavshows`

2. Run the app:

	`flask run`



## Project specifications

#### Authentification
Each user can create an account with a username, an email address and a password.
Then, the user will be able to log in each time he goes to the website.
You are welcomed to create your own account by clicking on the "register" button.
If you are in a rush, here are some credentials for a prefilled account :

- username: jules
- password: password

#### My favourites
Each user can add and remove TV shows from his favourites.
To do it, he has to be connected. Once logged in, he can do these actions by simply clicking on the heart icon.
You are welcomed to add and remove all your favourite shows.

#### Notifications
Each user will be notified if one of his favourite shows is currently running whenever he goes to his favourites page or the said show page.
You are welcomed to see this notification by adding to your favourites the show named "The Walking Dead" for example, or any other currently airing show you might think of.

#### Object oriented programming
All the results of our API requests are stored in Python objects.
We have created 3 main classes :

- one Show class
- one Season class
- one Episode class

For each class, there is a subclass that inherits it, for example the ShowDetailedView class. The subclasses complete our objects with a more precise API request.
All our attributes are in private or protected status according to their use. We have defined properties for all of them.

#### Errors and exceptions
When an error occurs, an exception is raised for the developers and the final user is redirected to an error page. 
The following errors are handled by our code:

- the API is down : We created the APIerror exception to handle the case of a disfunctionning API.
- the API results have changed : some arguments have been deleted or their type have changed for example

#### Multithreading
We thought that it was useful to implement multithreading when the user loads his favourites page. Indeed, we noticed that we had to make as many API calls as the number of favourite TV shows, and that process could be pretty slow.
Therefore we made sure that each of this request will be launched by a single thread, and at the same time than the others (cf class APIrequest(Thread) in classes.py and function make_multi_requests in backend.py).
Your are welcomed to add a few TV shows to your favourites and note how quick the favourites page loads.

#### Our originality
We made sure that the graphical interface could be as intuitive and beautiful as it could be.
We added a few custom features to the application to improve user experience such as:

- a user can easily discover new tv shows by surfing on the different pages: trending, popular, top rated
- whenever a signed user has at least one show in his favourites, he gets recommandations on the home page relating to the last show he added in his list
- we made sure that the user could easily switch between the different result pages
- the user can use the right and left arrow keys on the search results, trending, popular and top rated pages

