# A Backend Server for a Wn/Ln Series Translation Service

## Description

This project is developed partly out of boredom, and partly to dust my github account. This project is aimed to be used in my webnovel/lightnovel translation (site? app? still not sure).

## Technologies Used
 - **Python** as main programming language,
 - **Django** as *backend framework*,
 - **Docker** for ease of deployment ~~and to not make a mess on my main python env again cuz i forgot to use venv again~~.

## How to Run/Set up

**wait, really?**

Well, you only need **Docker**, and an **internet connection** i think.

  1. run the following command in root project folder.
    ```shell
        docker build .
    ```
  2. run the following command after the docker image is successfully build.
    ```shell
        docker compose up
    ```
  3. *go inside* the docker container using
    ```shell
        docker exec -it translations_web bash
    ``` 
  4. run the *migrations* using
    ```shell
        python manage.py migrate
    ```
  5. to *browse* currently availabe endpoints, go to *localhost:8000/api-explorer/*