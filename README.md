### Hexlet tests and linter status:
[![Actions Status](https://github.com/mnogom/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/mnogom/python-project-lvl4/actions)
[![python-ci](https://github.com/mnogom/python-project-lvl4/actions/workflows/python-ci.yaml/badge.svg)](https://github.com/mnogom/python-project-lvl4/actions/workflows/python-ci.yaml)
[![Maintainability](https://api.codeclimate.com/v1/badges/e026833e3bf6310ae6ff/maintainability)](https://codeclimate.com/github/mnogom/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e026833e3bf6310ae6ff/test_coverage)](https://codeclimate.com/github/mnogom/python-project-lvl4/test_coverage)

---
#### Heroku cheat sheet

##### Config env
* DISABLE_COLLECTSTATIC: 0
* DISABLE_POETRY_CREATE_RUNTIME_FILE: 1 _to protect build from crashes \[?\]_
* ENV: production
* SECRET_KEY: some-secret-key

попробовать поставить в .env

```sequence
Alice->Bob: Hello Bob, how are you?
Note right of Bob: Bob thinks
Bob-->Alice: I am good thanks!
```