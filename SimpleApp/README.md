<h1 align="center">
  SANIC SIMPLE API
</h1>

### What’s In This Document

---

- [Quickstart](#quickstart)
- [Reference](#reference)

---

### :rocket: Quickstart <a name="quickstart"></a>

Project provide two mode environments is development and production, the development environment used when development
process and the production environment used to deployed in server
You can run the project on your local environment with these steps:

1. **Setup python virtual environment and install libraries**

- *To create virtual environment, run command:*

    ```shell
    python3 -m venv venv
    ```
  Or you can use Add Interpreter in PyCharm

- *Activity virtual environment in ubuntu:*
    ```shell
    source venv/bin/activate
    ```
- *Install libraries*
    ```shell
    pip3 install -r requirements.txt
    ```

2. **Start Trava API in `development` mode** <br />
   To start API with development environment, simply you run

    ```shell
    make rundev
    ```

   If you want to run project with custom environment, you run following:

    ```shell
    make rundocker
    ```

   You want to run project directly without docker, run following:

    ```shell
    make run
    ```

- to get more information, you can run:
    ```shell
    make help
    ```

- After your app ran, you can follow [here](http://0.0.0.0:8000/swagger/) to test api

---

### Database testing

- How to execute database docker container

    ```shell
    docker exec -it dev_sanic_sql_container bash
    ```

- Login default user with password is sanic

    ```shell
    mysql -u root -p
    ```

- Switching to sanic_app database

    ```shell
    use sanic_app;
    ```

- End then you can enter your query command in console line.

---

### Reference <a name="reference"></a>

- [https://core.telegram.org/bots/api#available-methods](https://core.telegram.org/bots/api#available-methods)
