# IT-project-Belov-Isakov-2021

# Deployment to Heroku
Full info: https://devcenter.heroku.com/articles/getting-started-with-python

In short, do in terminal:
1. > heroku login
2. > heroku create
3. > heroku config:set TOKEN="<...data here...>"
4. > git push heroku main
5. > heroku open
6. if something went wrong,
   > heroku logs --tail
