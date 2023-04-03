# WeirdGame

Aiming to hit the backend of a Shakes and Fidget game (closer to Knights, but way less popular). Basicly you have a character and you can fight monsters (fight simulation), go into the gold mine for X hours, maybe do some quests.

Weird instructions for localhost run (anyone needs them?):
1. Set ALLOWED_HOSTS in mysite/settings.py to your address.
2. Go into the main folder and run command "python manage.py runserver 0.0.0.0:8000" to start on localhost with 8000 port.
3. On the main page you can choose to register and login.
4. After logging in your character is created with the name == login.
