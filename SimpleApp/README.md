<h1 align="center">
  SANIC SIMPLE API
</h1>

### What’s In This Document

---

1. [Quickstart](#quickstart)
2. [Database testing](#database_testing)
3. [Reference](#reference)

---

### :rocket: Quickstart <a name="quickstart"></a>

Project provide two mode environments is development and production, the development environment used when development
process and the production environment used to deployed in server
You can run the project on your local environment with these steps:

1. **Setup python virtual environment and install libraries**

- _To create virtual environment, run command:_

  ```shell
  python3 -m venv venv
  ```

  Or you can use Add Interpreter in PyCharm

- _Activity virtual environment in ubuntu:_
  ```shell
  source venv/bin/activate
  ```
- _Install libraries_
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

### Database testing <a name="database_testing"></a>

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

### Pre commit <a name="pre_commit"></a>

My project use [pre-commit](https://pre-commit.com/#intro) to check code before pushing to git. You can find all setup and command line in [here](https://pre-commit.com/#intro). In this article, i simply introduce some useful command line

- Install pre-commit to git hook

```commandline
pre-commit install
```

- Run pre-commit manually

```commandline
pre-commit run --all-files
```

- Learn command line rule

```commandline
pre-commit --help
```

---

### Reference <a name="reference"></a>

- https://core.telegram.org/bots/api#available-methods
- https://pre-commit.com/#intro
