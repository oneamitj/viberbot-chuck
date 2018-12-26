# About
A simple viber bot created in python3 and deployed in heroku container.

# Usage
1. Login to [Viber Partners](https://partners.viber.com/) and create Bot Account. Check for Token in Account Info.
2. `git@github.com:wannamit/viberbot-chuck.git` and `cd viberbot-chuck`
4. [Install Heroku](https://devcenter.heroku.com/articles/heroku-cli)
5. Setup Heroku account
	1. Login Heroku
	2. Create new pipeline (No need to connect to github)
	3. Create new app (app name required later)
6. Replace 4 strings in `viberChuckBot.py`
	1. `MY_BOT_NAME` => Name of your Bot Account
    2. `MY_IMAGE_URL` => URL of your Bot Acccount Image
    3. `MY_APP_TOKEN` => Bot Account Token provided in Account Info
    4. `HEROKU_APP_URL` => https://<heroku_app_name>.herokuapp.com
7. Login Heroku in local Terminal `heroku login`
8. Install Docker [Help](https://docs.docker.com/install/)
9. Pull python image used here `docker pull python:3-alpine3.7`
10. Heroku Container Login `heroku container:login`
11. Create docker image and push to heroku `heroku container:push web -a <heroku_app_name>` (keep the name `web`)
12. Release pushed docker image `heroku container:release web -a <heroku_app_name>`
13. Open Heroku App's > Resources > Change Dyno Type > Turn ON `web` dyno
14. Scale `web` dyno `heroku ps:scale web=1 -a <heroku_app_name>`
15. Open app (Top right of Heroku App page). Should reply "Viber bot that gives Chuck Norris joke as reply of each message."
16. To check Heroku server logs `heroku logs --tail -a <heroku_app_name>`
17. Check your Public Account Viber Bot in Viber; It should now have option to send message.
18. Send any message to bot and it will reply with random Chuck Norris Facts
19. An example [here](https://chats.viber.com/chucknfacts/)