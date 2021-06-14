# Playlist

## 1. About app
Playlist is DB SQL app made to keep data about movies. This app was made because a lot of people are in interested in movie culture and now in Covid-19 times movies are safe type of hobby.
#### 1.a What does app do?
This app is used to maintain a SQL DB with information about movies. The configuration panel, available for signed users, allows them to dynamically increase the number of selections as they type in forms about movies. The app allows you to add comments and grades about your movies. Displayed grade is the average of grades given by users. Each user can change his grade. Data entered by the user can be changed by its author. Movie data are displayed in order of Newest, Best, or Most Popular movie.

#### 1.b Differences and why?
- responsive for mobile devices - to make the application more universal
- data storage in several tables - to allow cascading deletion and not to create orphan data
- config panel - not only the admin extends the app, some modifications can be add by signed user.
- single-page application - almost, 99% of the app's features are hosted in index.html

#### 1.c Complexity and what is interesting in this app?
- guest mode - for unlogged user app becomes passive. That user can watch, read but can't change anything.
- cascade deleting - When user deletes one movie, he deletes also whole grades and comments for movie.
- easy to expand - very easy to add new tables, functions and panels
- dynamic forms - the choices depend on the data stored in the DB
- configuration panel - allows users to add new options to forms, not only via admin

## 2. How to run Requirements
- Python 3.8.5
- Django 3.1.5
- Ubuntu 20.02.2 LTS  - written in this OS.

## 3. How to run
Unzip and in terminal enter file project5, then type:  
python3 manage.py runserver

## 4. Files
In this app I have created new 9 files, rest is pure Django.
#### 4.a urls.py
Url addresses for functions in views.py. Most important is index with url '/', the major function in app. There are addresses for functions login/register user functions , CRUD functions for movie, grade, comment and sorting selectors.

#### 4.b models.py
Tables in DB:
- User	- username and password - like in other projects
- Genere - keeps the genre name of the movie
- Movie - major data about movie. Movie table is in One-to-one relations with User and Genere tables.
- Coment - keeps text of single comment made by one user about single movie. It is in One-to-one relations with User and Movie tables.
- Grade - similar to Coment, but keeps grades.
- Actor - keeps actor names.
- ActorMovie - there is id of movie and id of actor. This table is to make Many-To-Many relation between Movie and Actor tables.

#### 4.c views.py
- login_view, logout_view, register - similar to other projects.
- config - shows config panel where registered can add new movie genre and actor.
- addgenere - adds a new movie genre, expands the number of options in the forms about movies
- addactor - adds a new actor, expands the number of options in the forms about movies
- index, addmovie, edit_movie, delete_movie - CRUD functions for Movie table. Movie model is the major data in this app. A movie grade is calculated by averaging the ratings given by users.
- addgrade - Creates new row in Grade table which shows what user gave what grade for single movie.
- edit_grade - Changes users grade about single movie and returns to index board. Each user can change the grade.
- edit_grade_com - Changes users grade about single movie and returns to board with comments.
- coment_index, addcoment, edit_coment, delete_coment - CRUD functions for movie comments. Those functions are used in board with comments.
- best - shows all movies in order from the highest grade
- mostpopular - shows all movies in order of highest number of grades
- takeSecond - gets the 2nd element from list, it is used in best function in views.py

#### 4.d index.js
This js file contains all js functions for this app:
- addmovie - It adds new row in Movie table.
- editmovie - It changes data in single row in Movie table.
- addgenere - It adds new name of genre in Genere table.
- addactor - It adds new name of actor in Actor table.
- addgrade - It adds new grade, user and movie ids in Grade table.
- editgrade - It changes grade in Grade table.
- addcoment - It adds new comment, user and movie ids in Coment table.
- editcoment - It changes comment text in Coment table.
- menu - to create active menu on the top of site.

#### 4.e layout.html
The main html file that is expanded by blocks from other html. Active menu is entered in layout.html and some parts of it are only included for signed users.

#### 4.f index.html
The longest html file in this app. Index.html is extension of layout.html, which appends the appropriate blocks of html code. The file has been divided into parts that are exposed depending on the enabled function in the app. Some parts are only visible to active users. The visible part is determined by the variable f (f = 1 - Shows the list of movies, index board; 2 - Form for adding a new movie;
 3 - configuration panel that allows signed user adding new actors and new movie genres; 4 - Panel with comments and details about a single movie; 6 - Movie editing form). Forms are created dynamically, adding a new actor or genre increases the choice. Grades can be greater than 1 and less than 5 with step = 0.1.


#### 4.g login.html and register.html
Similar to such files from other projects. They allow registration and sign in.

#### 4.h styles.css
This CSS file contains all the CSS tags for this app.


## 5. Mobile responsive
There are 3 screen sizes in the app: for desktop (width more than 775px), tablet (width between 775 and 600px)  and phone (width less then 600px). The data is centered on the page with equal margins on the right and left. The area of data boxes decreases as the screen decreases. On a small screen, the boxes with the data are arranged one above the other. The top navbar collapses to a width less than 775px. To expand it, just click the expand icon.
