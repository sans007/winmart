# winmart

<br>

# create a New environment

install virtualenv

```
pip install virtualenv
```

create environment

```
 python -m venv .venv

 #or

 virtualenv .venv
```

## activate the env

#### On Windows, run:

```
.venv/Scripts/activate

#or

source .venv/Scripts/activate
```

#### On Unix or MacOS, run:

```
source .venv/bin/activate
```

## deactivate

```
    deactivate
```

<br>

# install requirements tools

```
    pip install -r requirements.txt
```

# Run app
## development
```
python wsgi.py
```
## production
```
# start command ------------------------------------------------

# waitress
    waitress-serve wsgi:app
        or
    waitress-serve --listen=127.0.0.1:5000 wsgi:app
        or
    waitress-serve --host 0.0.0.0 --port 5000 wsgi:app

# gunicorn 
    gunicorn wsgi:app
        or
    gunicorn --bind 0.0.0.0:5000 wsgi:app
```
