# TradingApp
App to Track and Analyze Trades Taken on a Daily, Weekly, Monthly and Yearly Basis

The App's First Version will consist of the following...

1. MySQL Database
2. Python Back End
3. React Front End

There will be a few different pages that will be served to the user
1. Login Screen - This is where the user will either log in or create a user for the first time
2. Dashboard Screen - This will provide an overall summary of all trades, total pnl, total trades logged, total pnl % etc etc
3. Trade Log Screen - This is where the user will go to view the log of all trades, notebook/journal style with the ability to reflect and add commments like someone would in a journal
4. Analysis Page - This is where the user can apply filters and other such things to their trades, organize by week/month/day/year whatever you would like, look at specific trade types. This is where the logic and creativity comes in to couple with trade analysis to provide the user with edge
5. Calendar Page - This is where you view you pnl in a calendar type view so you can visually get a sense for how tthe week/month/year is going. This could possibly be added to the Trade Log Page but not sure yet

Quickstart/Deployment Guide:
  1. Pull Code:
      - git clone https://github.com/Jpalm20/TradingApp.git
  2. Database
      - Create Local DB with name "TradingApp"
      - Grab the DDL files from repo and create Trade and User table
      - Go to src/models/utils.py and insert you credentials for the DB connection
  3. Docker:
      - docker build --tag trading_app . 
      - docker run -d -p 8080:5000 trading_app
  4. Run FE
      - go to client folder in terminal
      - npm run start
  5. Register a User
      - Click Sign Up link on login page when you land on app
      - Fille out info, save login info
  6. Login
      - You should be returned to login page after registering successfully
      - Use login info and now you are in app
