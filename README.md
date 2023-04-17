# WeirdGame

Aiming to hit the backend of a Shakes and Fidget game (closer to Knights, but way less popular). Basicly you have a character and you can fight monsters (fight simulation), go into the gold mine for X hours, maybe do some quests.

Weird instructions for localhost run (anyone needs them?):
1. Set ALLOWED_HOSTS in mysite/settings.py to your address.
2. Set your database or use default sqlite.
3. First run needs database migrations with "python manage.py migrate"
4. Go into the main folder and run command "python manage.py runserver 0.0.0.0:8000" to start on localhost with 8000 port.
5. On the main page you can choose to register and login.
6. After logging in your character is created with the name == login.

OR JUST FOLLOW THE **[LINK](https://weirdgame.onrender.com/)** (why did I not start with this?)
Both Postgresql and Django servers are free, so they go down if not used for a while. If the site isn't loading instantly, it's probably because the server is starting.
Anyways if it's not working it means I messed something up. In this case only hire me at your own risk.

This is my Text!
