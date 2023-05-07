<div>

[]{.c10 .c29}

</div>

# [Blog-Lite v2 Report]{.c10 .c16 .c31}

------------------------------------------------------------------------

[]{.c10 .c16 .c33}

## [Description:]{.c6}

[Blog-Lite is a web-based application made with Vue3 and Python-Flask.
It enables multiple users to share their ideas in the form of text-based
blog entries accompanied by a suitable image. It facilitates users to
follow and search other bloggers, and express their views by commenting
on their posts. Additionally, a Rest API has been developed adhering to
the OpenAPI Specifications, which permits access to the app\'s database
for limited data modification purposes.]{.c21}

## [Technologies Used:]{.c6}

-   [Python: ]{.c5}[responsible for developing the controllers and
    serving as the host programming language for the app]{.c3}
-   [Vue.js: ]{.c5}[used to develop the front-end of the app]{.c3}
-   [HTML: ]{.c5}[responsible for developing the required Vue components
    and templates]{.c3}
-   [CSS: ]{.c5}[responsible for styling the web-pages]{.c3}
-   [Bootstrap: ]{.c5}[used to make the front-end appealing and easy to
    navigate]{.c3}
-   [SQLite: ]{.c5}[serves as the database for the app]{.c3}
-   [Flask: ]{.c5}[serves as the web-framework for the app]{.c3}
-   [Flask-Restful: ]{.c5}[used to develop the RESTful API for the
    app]{.c3}
-   [Flask-SQLAlchemy: ]{.c5}[used to access and modify the app\'s
    SQLite database]{.c3}
-   [Flask-Celery]{.c5}[: used for asynchronous background jobs at the
    backend]{.c3}
-   [Flask-Caching]{.c5}[: used for caching API outputs and increasing
    performance]{.c3}
-   [Redis]{.c5}[: used as an in-memory database for the API cache and
    as a message broker for celery]{.c3}
-   [Swagger OpenAPI: ]{.c5}[used to create the documentation for the
    API developed for the app]{.c3}
-   [Seaborn: ]{.c5}[used to]{.c21}[ ]{.c5}[create the various required
    charts]{.c3}
-   [Git: ]{.c5}[responsible for version control]{.c3}

## [Database Schema:]{.c6}

[The database has four tables and the schema is as follows:]{.c3}

[]{#t.720d9c3e773a71bfbee745aee3c2b4dbdb1cb818}[]{#t.0}

+-----------------------------------+-----------------------------------+
| [User Table]{.c10 .c5}            | [Post]{.c11}[ Table]{.c5 .c10}    |
+-----------------------------------+-----------------------------------+
| -   [Roll]{.c5}[ (Integer):       | -   [Roll]{.c5}[ (Integer):       |
|     Primary Key, Auto             |     Primary Key, Auto             |
|     Increment]{.c3}               |     Increment]{.c3}               |
| -   [Username]{.c5}[ (String):    | -   [Author]{.c5}[ (String):      |
|     Unique, Not Null]{.c3}        |     Foreign Key (User.roll), Not  |
| -   [Email]{.c5}[ (String):       |     Null]{.c3}                    |
|     Unique, Not Null]{.c3}        | -   [Img]{.c5}[ (String): Not     |
| -   [Password]{.c5}[ (String):    |     Null]{.c3}                    |
|     Unique, Not Null]{.c3}        | -   [Text]{.c5}[ (String): Not    |
| -   [Img]{.c5}[ (String): Not     |     Null]{.c3}                    |
|     Null, Default 0]{.c3}         | -   [Date ]{.c5}[(String): Not    |
| -   [PDF ]{.c5}[(Integer): Not    |     Null]{.c3}                    |
|     Null, Default 0]{.c3}         | -   [Title ]{.c5}[(String): Not   |
|                                   |     Null]{.c3}                    |
|                                   | -   [Views ]{.c5}[(Integer): Not  |
|                                   |     Null, Default 0]{.c3}         |
|                                   | -   [Likes ]{.c5}[(Integer): Not  |
|                                   |     Null, Default 0]{.c3}         |
+-----------------------------------+-----------------------------------+

[]{.c3}

[]{.c3}

[]{.c3}

[]{.c3}

[]{#t.b9beb8a107c49ccdeeb8a654f9a58605618b9870}[]{#t.1}

+-----------------------------------+-----------------------------------+
| [Comment Table]{.c10 .c11}        | [Follow]{.c5}[ Table]{.c10 .c11}  |
+-----------------------------------+-----------------------------------+
| -   [Roll]{.c5}[ (Integer):       | -   [Roll]{.c5}[ (Integer):       |
|     Primary Key, Auto             |     Primary Key, Auto             |
|     Increment]{.c3}               |     Increment]{.c3}               |
| -   [Post]{.c5}[ (Integer):       | -   [Following]{.c5}[ (Integer):  |
|     Foreign Key (Post.roll), Not  |     Foreign Key (User.username),  |
|     Null]{.c3}                    |     Not Null]{.c3}                |
| -   [Author]{.c5}[ (String):      | -   [Follower ]{.c5}[(String):    |
|     Foreign Key (User.username),  |     Foreign Key (User.username),  |
|     Not Null]{.c3}                |     Not Null]{.c21}               |
| -   [Comment]{.c5}[ (String): Not |                                   |
|     Null]{.c21}                   |                                   |
+-----------------------------------+-----------------------------------+

[]{.c6}

## [API Design:]{.c16}

[The Flask-Restful library for Python was used to create a RESTful API
adhering to the OpenAPI Specifications. All database tables have CRUD
operations available through the API. Authentication tokens are used for
specific requests that require them. These tokens can only be obtained
from the user\'s account page when signed in. For further details,
please refer to the openapi.yaml file.]{.c3}

## [Architecture and Features:]{.c6}

[The architecture of Blog-lite follows a client-server model, where
Vue.js serves as the front-end framework and Python-Flask as the
back-end framework. Vue.js handles the presentation layer and manages
user interactions through its MVVM architecture, while Python-Flask
handles the server-side logic, such as HTTP requests and responses,
asynchronous tasks, and database interactions. ]{.c3}

[The features of the application are as follows:]{.c3}

-   [User authentication]{.c5}[: Signup and Login]{.c3}
-   [User profile]{.c5}[: View own posts, followers, and follows]{.c3}
-   [Explore other users]{.c5}[: View their posts, followers, and
    follows]{.c3}
-   [User-specific API tokens]{.c5}[: Generate tokens to use
    user-specific requests]{.c3}
-   [Post analytics]{.c5}[: View clicks, likes, and comments on
    posts]{.c3}
-   [Data export]{.c5}[: Download user\'s posts and analytics as a CSV
    file]{.c3}
-   [Social features]{.c5}[: Search, follow, and unfollow other
    users]{.c3}
-   [Personalized feed]{.c5}[: View posts from followed users]{.c3}
-   [Content management]{.c5}[: Create, view, edit, and delete
    posts]{.c3}
-   [Account management]{.c5}[: Create, view, edit, and delete user
    accounts]{.c3}
-   [User feedback]{.c5}[: Comment and like posts to express
    opinions]{.c3}
-   [RESTful API]{.c5}[: API available for posts, users, comments, and
    follows]{.c3}
-   [Import blogs: ]{.c5}[Ability to import blogs in bulk]{.c3}
-   [Export blogs]{.c5}[: Export blog content as PDFs]{.c3}
-   [Reminders]{.c5}[: Receive daily reminders to post]{.c3}
-   [Monthly engagement report]{.c5}[: Receive a report as an email or
    PDF summarizing engagement for the month]{.c3}
-   [Mobile Interface]{.c5}[: Adaptive Interface for devices of various
    sizes and shapes]{.c3}
-   [PWA Installation]{.c5}[: The app can be installed on various
    devices as an app for offline browsing]{.c3}

## [Video:]{.c6}

[For the video, click ]{.c21}[[here](https://www.google.com/url?q=https://drive.google.com/file/d/1m0fumBfuETH1ZQDZ2E0Zuaw2iBo1-d8x/view?usp%3Dsharing&sa=D&source=editors&ust=1683445069741509&usg=AOvVaw0fnfjhmc2tXnEVbNcs3I4o){.c20}]{.c21
.c32}[!]{.c21}

## Instructions for running the application

1. Navigate to the root folder of the application.
2. Open two separate terminals and execute the following commands in each:

    * `redis-server`
    * `mailhog`
3. Navigate to the backend folder and open three separate terminals. Execute the following commands in each:

    * `python main.py`
    * `celery -A main.celery worker -l info`
    * `celery -A main.celery beat --max-interval 1 -l info`
4. Navigate to the frontend folder.
5. In the terminal, execute the following command:

    * `serve -s dist`

These steps will successfully run the application, allowing you to access it from your web browser at [http://localhost:3000](http://localhost:3000).