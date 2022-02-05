# IT-project-Belov-Isakov-2021

# Deployment to Heroku
Full info: https://devcenter.heroku.com/articles/getting-started-with-python

In short:
1. Install heroku
2. Create new project in PyCharm from VCS https://github.com/NosayFN/IT-project-Belov-Isakov-2021.git
3. Do in terminal:
   
   To create new instance:
   > heroku login
   > 
   > heroku create
   > 
   > heroku config:set TOKEN="<...data here...>"
   > 
   > git push heroku main
    
   To use existing instance:
   > heroku login
   > 
   > (...do some changes in code...)
   > 
   > git commit <...>
   > 
   > git push <...>
   > 
   > git push heroku main
   
   If something went wrong,
   > heroku logs --tail
   
   To open in browser:
   > heroku open

To open database:
1. Install PostgreSQL on local machine:
   > https://devcenter.heroku.com/articles/heroku-postgresql#set-up-postgres-on-windows
 
2. Open psql console:
   > heroku pg:psql

3. In case of problem with russian symbols, execute in psql console:
   > \! chcp 1251
