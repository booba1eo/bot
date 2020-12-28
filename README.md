# Development environment setup

### ngrok setup

- Download & setup ngrok,  see https://ngrok.com/download
- in the folder where ngrok is unpacked

```sh
./ngrok http 8000
```

### Django project setup

###### Work with python only in virtual environment
```sh
pip3 install virtualenv 
virtualenv venv --python=python3.7
source venv/bin/activate
cp setenv.sh.example setenv.sh
source setenv.sh
```
```
pip install -r requirements.txt
```
##### Docker(database) setup
- Download [docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
```sh
docker login
docker run --name bot-postgres -e POSTGRES_PASSWORD=$BOT_DB_PASSWORD -d -p 5432:5432 postgres:11
```

##### Start django server
-  Сheck `ngrok` is on
```sh
# in root folder
cd chatbot
pip install -e .[dev]
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 
```

### Facebook app setup
- Look [here](https://developers.facebook.com/docs/messenger-platform/getting-started/app-setup)
- add your `Page Access Token` in `setenv.sh`

- On step `Configure the webhook for your app`:

1. Check `ngrok` and `django` server is on
2. `Callback URL` should look like: `https://03b28850.ngrok.io/chatbot/webhook/`
3. Take `Verify Token` from `setenv.sh.example`


### Setup pre-commit hooks

- flake8 + pylint + crlint

```sh
chmod a+x pre-commit && cp pre-commit .git/hooks
```

### Set bot profile

```sh
python manage.py set_bot_profile
```

<!-- 
### Create docker image with python dependencies

```.env
docker login
docker build -t cldntm/bot:{version} -f bitbucket-pipelines.dockerfile .
docker push cldntm/bot:{version}
``` -->