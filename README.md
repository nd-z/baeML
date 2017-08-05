![baeML](https://i.imgur.com/rHwT8uD.png)

Hello there! Welcome to our project. If you're here, that means at least one thing is true:

+ We were unable to deploy our project due to practical concerns.
+ You want to have our source code on hand, and possibly improve our project.
	+ If this is the case, feel free to check out the project specifications Markdown file `overview.md` in the same directory as this README.
+ You're an employer who wants to give all of us cushy 6-figure jobs.
	+ Pls...

In any case, we're glad that you're interested! Briefly, we started this project with the goal of breaking the so-called echo-chamber effect of social media. We aim to deliver content that appeals to your interests but avoids reinforcing your echo chamber. We hope that you find this helpful, if not a fresher take on news delivery platforms.

And so, we have this lovely little guide on how to build and run baeML. We hope it is as fun as it is easy to follow.

# Install and Run from Source
## Install the Packages
To get our project repo onto your computer (assuming you have Git installed on your computer), clone the repository into a directory of your choice.

`git clone https://github.com/jz359/baeML.git`

Then, go into the baeML folder (your shell commands might be different)

`cd baeML`

And install all the required Python packages (this may take a while)

`./dependencies.sh`


Note: There is a chance that we may have missed a package or two, and running the backend/frontend may give you a complaint about such packages. If this happens, simply run `pip install <missing package name>` and notify us so we can add that to the list!

Further Note: This also assumes you have Node.js and the package manager `npm` installed.

More Notes: You also need PostgreSQL installed. It's all straightforward stuff though, so no worries.

## Running the Server
The server is what makes everything work! But before that, we need to set up the database.

It's quite easy! Run these commands:

`psql postgres`

`CREATE ROLE admin;`

`CREATE DATABASE baeml_db OWNER admin;`

`\q`

Now, depending on how you installed PostgreSQL, there are different ways to run the database server. 

If you used Homebrew to install it, the command is `brew services start postgresql`
+ Intuitively, the command to stop the server is `brew services stop postgresql`
	+ It might be intuitive to you, but I didn't know this and suffered greatly.

If you used a different way, uh, we don't really know, but Google does!

Now we can start up our own server! Navigate to the server directory. From `/baeML`, it goes:

`cd backend/server/`

(Make sure to use the tab key to avoid typing too much and getting carpal tunnel)

Make the necessary migrations (or whatever) to the database you just created by running

`python manage.py makemigrations`

`python manage.py migrate`

AND NOW WE RUN THE SERVER

`python manage.py runserver localhost:3333`

Technically now you can just use the app via Postman and our very nice and documented Apiary API thing. But that's pretty boring, and it would make Eric and Janice really sad because they went through the trouble of learning (and using!!) React to give you a really nice user experience. So, we continue onto...

## Running the Frontend
Navigate back to the `/baeML` directory. From there, go to the `index` folder via

`cd index`

Unlike the backend, the frontend is very straightforward to run (if you have installed Node and npm like we told you to)

`npm install` (if you're running this for the first time)

`npm start`

Voila! Now you have the frontend running and connected to the backend! You'll notice an option (it's not really an option, you kinda have to do it) to sign in with your Facebook account. Do that, and you'll be directed to a waiting page.

You know how a bunch of websites tell you the loading part might take a while, but you never really expect it to? Well we actually need a few minutes because we have this really fancy M A C H I N E L E A R N I N G model that we need to load and use to deliver wonderful relevant content to you. So please don't think that our code is super bad and that it doesn't work!

Anyway, when the backend is done doing its magic, you will see the wonderful setup that we have created for you to consume your personalized content. It's quite uncomplicated, but hey, we're just students working for fun. If you want to incentivize us, we take anything from food, money, gum, even the stray cat in your backyard.

If you use this often enough, you might notice that it will take reaaaaallllyyyy long to get your next article. That's because we have a wonderful M A C H I N E L E A R N I N G model trying its very best to adjust itself to your tastes (however weird they might be). So please don't think that our code is super bad and that it doesn't work!

Anyway, that's basically the gig. We hope this README wasn't as boring as some of the other ones that Andy had to go through this summer. We would also like to stress that if this README gave you the wrong impression about its author, it's Andy's fault for not being funnier.