# Task Manager
Create user, add statuses and labels. Be ready to create tasks
> Demo: https://hidden-bayou-30395.herokuapp.com/

---
### Hexlet tests and linter status:
[![Actions Status](https://github.com/mnogom/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/mnogom/python-project-lvl4/actions)
[![python-ci](https://github.com/mnogom/python-project-lvl4/actions/workflows/python-ci.yaml/badge.svg)](https://github.com/mnogom/python-project-lvl4/actions/workflows/python-ci.yaml)
[![Maintainability](https://api.codeclimate.com/v1/badges/e026833e3bf6310ae6ff/maintainability)](https://codeclimate.com/github/mnogom/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e026833e3bf6310ae6ff/test_coverage)](https://codeclimate.com/github/mnogom/python-project-lvl4/test_coverage)
---
### Installation
```commandline
% git clone https://github.com/mnogom/python-project-lvl4.git
% cd python-project-lvl4
% make install
% make migrate
```

[comment]: <> (* to deploying to heroku &#40;with [heroku cli]&#40;https://devcenter.heroku.com/articles/heroku-cli&#41;&#41;)
[comment]: <> (```commandline)
[comment]: <> (% heroku config:set DATABASE_URL=postgres://...)
[comment]: <> (% heroku config:set DISABLE_COLLECTSTATIC=0)
[comment]: <> (% heroku config:set DISABLE_POETRY_CREATE_RUNTIME_FILE=1)
[comment]: <> (% heroku config:set ENV=production)
[comment]: <> (% heroku config:set ROLLBAR_ACCESS_TOKEN=rollbar-api-token)
[comment]: <> (% heroku config:set SECRET_KEY=some-strong-secret-key)
[comment]: <> (% heroku config:set ALLOWED_HOSTS=hidden-bayou-30395.herokuapp.com)
[comment]: <> (```)

#### Tests
To check if everything ok:
```commandline
% make test
```

---
### Models
Models
```
╔═════════════╗ ╔═════════════╗ ╔═════════════╗
║ Task        ║ ║ TaskLabel   ║ ║ Label       ║
╠═════════════╣ ╠═════════════╣ ╠═════════════╣
║ name        ║ ║ task        ║ ║ name        ║
║ description ║ ║ label       ║ ║ created_at  ║
║ [a]uthor    ║ ╚═════════════╝ ╚═════════════╝
║ [e]xecutor  ║ ╔═════════════╗
║ [s]tatus    ║ ║ Status      ║
║ [l]abels    ║ ╠═════════════╣
║ created_at  ║ ║ name        ║
╚═════════════╝ ║ description ║
╔═════════════╗ ║ created_at  ║
║ User        ║ ╚═════════════╝
╠═════════════╣
║ username    ║
║ email       ║
║ first_name  ║
║ last_name   ║
║ password*   ║
╚═════════════╝
```
Relation Ontology
```
╔═════════════╗   ╔═════════════╗   ╔═════════════╗
║ Task        l───╢ TaskLabel   ╟───╢ Label       ║
╚═══ s e a ═══╝   ╚═════════════╝   ╚═════════════╝
     │ │ │ ╔═════════════╗           
     │ │ └─╢ User        ║           
     │ │   ╚═════════════╝           
     │ │   ╔═════════════╗
     │ └───╢ User        ║
     │     ╚═════════════╝
╔════╧════════╗
║ Status      ║
╚═════════════╝
```

---

### Site map

* Home
  * `GET /` - index page
* CRUD Users
  * `GET /users/` - page with all users
  * `GET /users/create/` - page to create new user
  * `POST /users/create/` - creating new user
  * `GET /users/<int:pk>/update/` - page to update user
  * `POST /users/<int:pk>/update/` - updating user
  * `GET /users/<int:pk>/delete/` - page to delete user
  * `POST /users/<int:pk>/delete/` - deleting user
  * `GET /login/` - login page
  * `POST /login/` - authentication user
  * `POST /logout/` - logout user
* CRUD Statuses
  * `GET /statuses/` - page with all statuses
  * `GET /statuses/create/` - page to create new status
  * `POST /statuses/create/` - creating new status
  * `GET /statuses/<int:pk>/update/` - page to update status
  * `POST /statuses/<int:pk>/update/` - updating status
  * `GET /statuses/<int:pk>/delete/` - page to delete status
  * `POST /statuses/<int:pk>/delete/` - deleting status
* CRUD Labels
  * `GET /labels/` - page with all labels
  * `GET /labels/create/` - page to create new label
  * `POST /labels/create/` - creating new label
  * `GET /labels/<int:pk>/update/` - page to update label
  * `POST /labels/<int:pk>/update/` - updating label
  * `GET /labels/<int:pk>/delete/` - page to delete label
  * `POST /labels/<int:pk>/delete/` - deleting label
* CRUD Tasks
  * `GET /tasks/` - page with all tasks
  * `GET /tasks/create/` - page to create new task
  * `POST /tasks/create/` - creating new task
  * `GET /tasks/<int:pk>/update/` - page to update task
  * `POST /tasks/<int:pk>/update/` - updating task
  * `GET /tasks/<int:pk>/delete/` - page to delete task
  * `POST /tasks/<int:pk>/delete/` - deleting task
  * `GET /tasks/<int:pk>/` - page with detailed task

