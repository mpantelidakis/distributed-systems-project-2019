# distributed-systems-project-2019

clone the repository,
add the .env and .env.db files to the root folder

 run `docker-compose up`

available urls:

- localhost:8080
  - homepage
  - login
  - logout

- localhost:8080/friends
  - manage friends

- localhost:8080/friends/{slug}
  - view friend profile page

- localhost:8080/galleries
  - view all available galleries

- localhost:8080/galleries/{id}
  - view the images and comments for gallery with id {id}

##### To view the contents of a gallery u have to add the gallery's owner to your friends.

##### The Django rest browsable api endpoints are available under localhost:8080/api

### TODO LIST:

- [ ] Finish the frontend

- [ ] Add Zookeeper

- [ ] Remove all js from the templates and import it

- [ ] Use django's template inheritance

- [ ] Write proper css :muscle:
