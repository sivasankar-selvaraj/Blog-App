Blog Application
================
 It's simple blog application. This application have following functionality
  -> Register new user 
  -> Login user
  -> Registered user can add, update, delete post
  -> Registered user can comment to the post
  -> view posts
  -> view comments for specific post

Installation
============
Cloning this repository to your machine, create a virtual environment and install the requirements.

[----- For Linux and Mac users ----]

	$ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

Running
=======
To run this app by using following command:

    (venv) $ python api.py
    * Restarting with stat
    * Debugger is active!
    * Debugger pin code: 875-250-943

Then from a different terminal window you can send requests.

Note : Please change config file based on your credentials 

API Documentation
=================
----------------
Register New User
-----------------
	curl -i -X POST -H "Content-Type: application/json" -d '{"username":"siva","password":"1234"}' http://127.0.0.1:5000/api/add/users

	curl -i -X POST -H "Content-Type: application/json" -d '{"username":"sankar","password":"test1234"}' http://127.0.0.1:5000/api/add/users

	curl -i -X POST -H "Content-Type: application/json" -d '{"username":"xxx","password":"1234test"}' http://127.0.0.1:5000/api/add/users

---------------
Create new Post
---------------
	curl -u siva:1234 -i -X POST -H "Content-Type: application/json" -d '{"title":"Hello World","body":"This my first blog"}' http://127.0.0.1:5000/api/add/post

	curl -u siva:1234 -i -X POST -H "Content-Type: application/json" -d '{"title":"My Second blog","body":"hello hai"}' http://127.0.0.1:5000/api/add/post

	curl -u siva:1234 -i -X POST -H "Content-Type: application/json" -d '{"title":"My Third blog","body":"Add Two Integers"}' http://127.0.0.1:5000/api/add/post


--------------
Create Comment
--------------
	curl -u siva:1234 -i -X POST -H "Content-Type: application/json" -d '{"comment":"Nice"}' http://127.0.0.1:5000/api/add/posts/1/comments

	curl -u sankar:test1234 -i -X POST -H "Content-Type: application/json" -d '{"comment":"Nice"}' http://127.0.0.1:5000/api/add/posts/2/comments

	curl -u sankar:test1234 -i -X POST -H "Content-Type: application/json" -d '{"comment":"Nice"}' http://127.0.0.1:5000/api/add/posts/3/comments

------------------------
Create thereaded Comment
------------------------
	curl -u siva:1234 -i -X POST -H "Content-Type: application/json" -d '{"comment":"why this is nice?"}' http://127.0.0.1:5000/api/add/posts/1/comments/1

	curl -u sankar:test1234 -i -X POST -H "Content-Type: application/json" -d '{"comment":"its Good to read"}' http://127.0.0.1:5000/api/add/posts/1/comments/4

	curl -u xxx:1234test -i -X POST -H "Content-Type: application/json" -d '{"comment":"im read it but nothing in this, than how u say nice"}' http://127.0.0.1:5000/api/add/posts/1/comments/5

--------------
View All Posts
--------------
	curl -u siva:1234 -i -X GET http://127.0.0.1:5000/api/posts

----------------------------------
View Comments for particular post
----------------------------------
	curl -u siva:1234 -i -X GET http://127.0.0.1:5000/api/comments/1

-----------
Update Post
-----------
	curl -u siva:1234 -i -X POST -H "Content-Type: application/json" -d '{"body":"hello"}' http://127.0.0.1:5000/api/update/posts/1

-----------
Delete Post
-----------
	curl -u siva:1234 -i -X GET http://127.0.0.1:5000/api/delete/posts/1