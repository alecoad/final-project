# Final Project for CS50x - FocusFive25
## by Andrew Coad

This is a task list application using Flask and a touch of JavaScript. Much of the structure was adapted from the CS50 Finance project seen here: https://finance.cs50.net

The inspiration for this web application came from several places:
  1. I read a random article several months ago involving career advice from billionaire Warren Buffet.
  2. I was contemplating ideas for a worthwhile final project to finally finish CS50!
  3. I was looking for a way to focus my approach to learning programming & web development.

FocusFive25 was created to help inspire and increase focus and productivity. Although the (current) end result is a pretty neat task list application, the original inpiration came from Warren Buffet’s so called “5-25” rule used to prioritize one's career goals.

The "5-25 Rule" basically goes like this:
  - Write a list of twenty-five of your career goals, then after some introspection choose the top five.
  - The twenty that you don’t choose are now your “anti-goals” -- goals you want to accomplish, but in reality, they are goals that are distracting you from your top five goals.
  - This "rule" is supposed to help you stay focused on your true goals.

When I started creating this app, my intent was to walk the user through the whole "5-25" process, beginning with twenty-five goals, selecting the top five, and then organizing all the goals into a TO-DO and TO-NOT-DO list. I showed my wife, and she said, “Twenty-five is a lot. Does it need to be that many?” Her insight helped me broaden the usefulness of the app, and the idea morphed into a straightforward task list that does exactly what I want it to do.

Say you have ten tasks you want to complete today. Choose two, and the other eight become your “anti-tasks” -- avoid them until you finish the two tasks you chose to focus on! And if you want, you can still follow the "5-25" process to create a list with your twenty-five career goals and select the top five to focus on.

On each task list page (`/task/<int:list_id>`), you can choose one or more tasks and perform any of the following:
  - Focus on the task, which turns the task green. (You can also 'unfocus' tasks as well.)
  - Complete the task, which removed the background color and strikes out the task.
  - Delete the task, which removes the task completely.
  - Add a task, which takes you to another page to input and submit another task to add to the list.
  - Delete the entire list, which asks you to confirm because you can't get it back!

All these options involve queries to a postgres database, so every list and task is stored in the database and attached to your user profile. See the code for more details, including the schema for the three tables in the database.

I also built authentication into the app, using some of what I learned from completing the CS50 Finance project and some of what I learned working through the Flask tutorial (https://flask.palletsprojects.com/en/1.1.x/tutorial/).

Overall, I am very happy with the result and I actually made my first real FocusFive25 task list today to help me focus on finishing this README!

## How to install on your local machine

Coming soon...
