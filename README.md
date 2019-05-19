# distributed-systems-project-2019

clone the repository,
add the .env and .env.db files

run docker-compose up

user registration is only possible via the api atm at localhost:1337/api/user/create

available urls:

localhost:1337  -homepage, login, logout

localhost:1337/friends  -manage friends

localhost:1337/friends/{slug} -view friend profile page
  
localhost:1337/galleries -view all available galleries

localhost:1337/galleries/{id} -view the images and comments for gallery with id {id}

to view the contents of a gallery u have to add the gallery's owner to your friends.
