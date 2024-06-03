# My TODO App

## Prerequisites

- Python 3.12
- Pip 23.2
- Docker 20.10
- docker-compose 2.10

Chances are you can roll with lower versions, I haven't checked that though

## Setup

- Clone this repo on your local machine
- Copy `dev.env.dist` into `dev.env` and replace the placeholders in that file
- If you want to use Weather API then you need to set up a Weather API key
  - To do so go to https://openweathermap.org/api
- Start the container
  - Build the docker container and start it 
    - `docker-compose up -d --build`
  - Run migrations 
    - `docker-compose exec web python manage.py migrate`
  - Create a superuser to access the admin panel 
    - `docker-compose exec web python manage.py createsuperuser`
- Access the app on `localhost:8080`
- Access the admin panel on `localhost:8080/admin`
  - Go there and add some locations for future use

## Troubleshooting

Anytime you need to completely wipe your database you can run `docker-compose down -v`
After doing so, you will need to repeat steps for building the container, running migrations, creating a superuser, and adding locations
