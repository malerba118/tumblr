# tumblr

This site is live [here](http://ec2-52-26-168-116.us-west-2.compute.amazonaws.com/)

**Note**: if you do not wish to register, you may log in to an existing account with the following credentials:
 
    username: user1
    password: password

Below is the ER Diagram I designed to outline the backend:

![alt tag](http://s22.postimg.org/epp33vo69/Tumblr_ER_Diagram_Idea_2_2.png)

**Overview**: This social media website utilizes Django for server-side processing. Django’s built in templating is used as well as handlebarsJS. JQuery is used for dom traversal and AJAX calls. The system features lazy loading so as to reduce bandwidth upon visiting pages containing extensive content. Liking and deleting are also asynchronous processes. A Summernote WYSIWYG editor is used for post creation. The project is hosted on an AWS EC2 instance running Ubuntu 14.04 and utilizing nginx as a static files/proxy server and gunicorn as the source code server. Git was used to track the project.

**Features**:
* create/reblog/delete posts
* like posts
* follow blogs
* newsfeed displaying posts belonging to followed blogs
* lazy loading
* edit own blog, including ability to change blog template
* tag posts
* search for tags
* browse randomly chosen blogs

**Most difficult**: Receiving json objects from server and doing dom manipulation to insert them on AJAX calls. After coding this up, it created too much of a mess so ultimately rendered html server side and sent the rendered html to the client. Bandwidth is obviously much greater using this method but simplified the code and in the application’s youth, performance should not be an issue.

**Most interesting**: Database schema, required a lot of thinking and planning but very interesting(activities sort of became a mess. utilized ER diagram and class diagram). Also making requests asynchronous was interesting. Efficiency is fun. 
