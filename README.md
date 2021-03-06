# The Video Game Diary

This is my final project for CS50’s Web Programming with Python and JavaScript.
It's a mobile responsive diary application that helps you keep track of your gaming journey, letting you record when you start playing the game, when you finish it, complete it, how much you've played it, and write a small review for yourself.
It's a website I personally need, something I'm going to use, keep developing and hopefully host for others to use!

It's different and more complex than the other projects because it uses a third party API (IGDB.com, making use of their extensive database of videogames data), CSS animations and Sass, a responsive design with Bootstrap elements such as Modals, and many other techniques (both taught in the course and self-taught) to create an application that is personal, easy to use and functional; it's designed to be your own diary, and be the best it can be at it.
It is its own application, so it's not a front-end for another website, nor a community driven Wiki website with simple listing of entries for everyone to see - it's not made for posting auctions, listings, or public posts for others to see (although making your diary public, as some sort of personal blog, is considered as a future feature), and it has more functionality with its APIs than the e-mail client project.

The files created are:
- views.py, the Python views file with most of the logic on the back-end;
- urls.py, the file which contains all the paths the website supports;
- models.py, where Django models are defined;
In the "templates/diary" folder:
- layout.html, a layout for most pages on this website;
- layoutlogin.html, a layout for the login and register pages, which has extra contents compared to layout.html;
- register.html, the account registration page;
- login.html, a simple login page;
- index.html, the landing page you see after logging in, letting you navigate to the other parts of the website and quickly add hours played to your currently playing games;
- view.html, the main diary view, where you can visualize your calendar of games started, finished and played at the time;
- entry.html, the diary entry view page, where you can see details on the particular entry you selected 
- add.html, the entry creation page, where you can search for a game on IGDB and add it to your diary;
In the "static/diary" folder:
- home.svg, a home icon used for the "back to index" button;
- list.svg, a list icon used for the "back to diary view" button;
- new.png, an icon for the "Add an Entry" index button;
- nocover.png, a placeholder image for when a game has no cover available on IGDB.com;
- style.css, the CSS file generated by Sass;
- style.scss, the main Sass file;
- view.png, an icon for the "View your Diary" index button.