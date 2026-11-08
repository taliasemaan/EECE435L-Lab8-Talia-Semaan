# EECE 435L Lab 8 - Docker and Containers

Solo project by Talia Semaan (AUB username: `tts09`), based on the Lab 5 Flask
user-management API. The project builds two images that share a persistent
SQLite database:

GitHub repository: https://github.com/taliasemaan/EECE435L-Lab8-Talia-Semaan

| Image | Container port | API |
| --- | ---: | --- |
| `tts09/lab8-talia_semaan:0.0.1-RELEASE` | 5000 | Lab 5 user-management API |
| `tts09/lab8-talia_semaan:0.0.2-RELEASE` | 3000 | `GET /get_users`, returns user names |

Docker repository names must be lowercase, so `Talia_Semaan` is written as
`talia_semaan` in the image names.

## Run both containers

From this directory, build both images and start the services:

```powershell
docker compose up --build
```

The Compose setup creates one named volume and initializes the shared database
before either API starts. Stop the services with `Ctrl+C`, then run
`docker compose down` to remove the containers. The named database volume is
preserved; `docker compose down --volumes` removes it.

## Verify the APIs

In another terminal:

```powershell
Invoke-RestMethod http://localhost:5000/api/users
Invoke-RestMethod http://localhost:3000/get_users
```

The second API returns a JSON array containing each user's name. To add a user,
send a JSON `POST` to `http://localhost:5000/api/users/add` with `name`, `email`,
`phone`, `address`, and `country`; both APIs read the same database volume.

The full Lab 5 API is also available through the Postman collection
`Flask_user_app.postman_collection.json`.

## Submission evidence

`Lab8-Activity1-Commands.docx` contains the Activity 1 command explanations and
screenshots, along with the Docker Desktop screenshots for both required image
tags. The original screenshots are also available in `screenshots/`.

## Build images separately

```powershell
docker build -t tts09/lab8-talia_semaan:0.0.1-RELEASE -f Dockerfile.lab5 .
docker build -t tts09/lab8-talia_semaan:0.0.2-RELEASE -f Dockerfile.get_users .
```

## Tests

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
```
