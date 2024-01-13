# Getting started

## Using Docker
The easiest way to run this application is to use Docker.
First create your own ```.env``` file, there is a template for this:
```
cp .env.example .env
```
Next, set the ports in the new ```.env``` file to your desired ports.
Now, from the root directory of the application, your should be able to run:
```
docker compose up
```
You should get something that looks like:
```
You can now view emission-app in the browser.
  Local:            http://localhost:XXXX
```
Where XXXX is the port specified for the front-end. Follow this link to view and interact with the front-end of the application.
You can also see the back-end by going to ```http://localhost:YYYY```, where YYYY is the port specified for the back-end.
