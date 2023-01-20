# PaddleBot
 
A Selenium sign-up bot that automatically registers for platform tennis courts. 

In ```Bot.py```, ```book_paddle_automated()``` uses Selenium to launch a Chrome window and navigate through the website to complete a booking. The function must log in, select a day from a drop down menu, select a time slot, and type user information to complete a booking. The function will return a String indicating either success or failure.

All registration data is stored in a private file invoking the ```Reservation``` class. These ```Reservation```s are imported in ```main.py``` and used in the ```book_paddle_automated()``` function in ```Bot.py```. Feedback is written to a .txt file. 

```Util.py``` contains methods to convert Reservation data to the correct form for Selenium's ```driver.find_element(...)``` to correctly navigate the website, which features a updating weekly calendar with only seven days available at a time. 

------------------------

### Launch Progress

I originally used 

```
schedule.every().day.at("20:14:00").do(court1)
schedule.every().day.at("20:14:20").do(court2)

while 1:
    schedule.run_pending()
```

to automate making the reservations. However, that aspect as since been removed, so when ```main.py``` is run, the tasks are completed immediately. I am instead scheduling the task using ```cron```. Moving forward, I want to find a way to schedule the task remotely, so I do not need to have my local machine open and running at a given time each week. 
