# Assignment Report 
### Group 4
### Max Von Klemperer (s*****), Bart Lunenborg (s****), Arnaud Van Hees (s5177766)

## Explanation of Requirements

### Requirement 1.1
The following list outlines where to go in the front-end application for the different parts of this requirement:
- **Retrieve**: Fetch Country Data section.
    - If there is no year input, then all available data for the country will be displayed. If there is a year input, the **timeframe** decides what data is displayed.  
    - The **timeframe** works as follows. You can input:
      - before: Gets the relevant country data **including and before** the specified year
      - equal: Gets the relevant country data **for** the specified year
      - after: Gets the relevant country data **including and after** the specified year
    - The **timeframe** value defaults to **after** if it is not specified. This applies to all places where a **timeframe** is prompted in the front-end application. 

- **Create**: Create Country Data section. 
  - To create a new entry for a country's data you fill in all fields and press the submit button.
- **Delete**: Delete Country Data section.
  - Deleting a country works by inputting either the country's name or ISO code and a year. When pressing delete all the country's data for that year is deleted. 
- **Update**: Update Country Data section.
  - To update a country you can find the country, either by name or ISO code, and change the fields of the country's data accordingly. 

### Requirement 1.2
The **Fetch Country Emissions Data** section of the front-end application fulfills this requirement. 

If there is no year specified in the search all available data for the country will be displayed. If a year is input, the data 
including and after that year will be displayed. 
### Requirement 1.3
The **Continent Temperature Change** section of the front-end application fulfills this requirement. 

If there is no year specified in the search all available data for the continent will be displayed. If a year is input, **timeframe** decides how the information will be displayed. 

### Requirement 1.4
The **Fetch Country Energy Data** section of the front-end application fulfills this requirement. 

Here we make use of Pagination to display the search results:
- **Number of Countries**: How many countries are displayed on a page. 
- **Page**: Which page should be displayed.
  - If no page is input, it defaults to the first page. 

### Requirement 1.5
The **Fetch Contribution To Climate Change Data by Country** fulfills this requirement. 

If both the specified year and the past year is input, the information will display the relevant countries for the specified year.

In the sort field you can specify if you want the information to display the **top** or **bottom** N countries.  

### Requirement 2
For the applicable API endpoints there is a checkbox that allows you to select CSV. If this checkbox is ticked the content-type 
of the data will be CSV. This is handled in the back-end of the application.
To better visualise the CSV data we have also formatted this data into a table. 

### Requirement 3
Our API design's documentation can be found in the APISpecification.yaml file. The **routers** package is where the documented 
code for the API endpoints is. The different API endpoints all have the following documentation where applicable:
- **Name**: The name of the endpoint
- **Return**: What the endpoint returns
- **Return representation**:The content-type of the data that is returned. This defaults to JSON. When CSV the content-type changes to CSV. 
- **Endpoint Access**: Operation type and route to execute/retrieve the specified operation. 
- **Query Parameters**: The parameters that are processed by the API in the request. Some of the parameters are optional and others are required for the request. 
- **Errors**: The errors that can arise in the process of making the request. 

### Requirement 4
To implement the back-end of our application we used the FastAPI framework which uses Python as the language. We have ensured to document the implementation code appropriately explaining functions and parts of code where necessary.

We use an SQL database and interact with it through SQLAlchemy. We use SQLAlchemy as it is well integrated with Python, allowing us to write and perform all queries needed easily and concisely.
Furthermore, a benefit of SQLAlchemy is that it is well documented, especially the Object Relational Mapper topic. This helped us a lot when writing the back-end of our application.  

### Requirement 5
The front-end of our application is created using React in Javascript. The main reason we decided to use React was for the component structure it offers. 
The components helped us a lot in maintaining an organised front-end. Not alone in the file structure but also in the creating of the web page.
The different sections of our front-end that showcase the API's functionalities are as mentioned in the **Requirements 1.** section of the report.  

### Requirement 6
This application can be run with `docker compose up` as per requirement 6.
These instructions will cover how to do this, assuming docker is installed an you are using Linux.

### Docker instructions
First create your own `.env` file using the template:
```
cp .env.example .env
```
Next, set the ports in the new `.env` file to your desired ports.
Now, from the root directory of the application, you should be able to run:
```
docker compose up
```
You should get something that looks like:
```
You can now view emission-app in the browser.
  Local:            http://localhost:XXXX
```
Where XXXX is the port specified for the front-end in the `.env` file. Follow this link to view and interact with the front-end of the application.
You can also see the back-end by going to `http://localhost:YYYY`, where YYYY is the port specified for the back-end in the `.env` file.


## Design & Framework rationale

## **Note to max and Bart**
I have already mentioned a little about why we use SQLAlchemy and React. We should expand on this. 

Why we choose python could be because we (Max and Bart?) were already familiar with it and we knew that Python was well documented. We followed along with a course/youtube tutorials for the backend. 

Then we should discuss some design choices that we made. Like explaining the routers and the services. I don't think we should talk too much about design for the front end. 


## Work Distribution and Roles
As a team we communicated a lot. Whether this was by doing in person work together or through messages on the Whatsapp chat, we 5constantly kept each-other updated on
what was happening from everyone's side. This helped us a lot as we could help each other out quickly. Overall, we feel the collaboration of the team was very good. 

Max was very dedicated to the project and did a big part of it. He implemented the majority of the back-end of the application. As well, he created the core components for the front-end application. 

Arnaud and Bart's roles were predominantly to finish up the back and front-end of the application. This meant we looked through the project description carefully and ensured the API design met all requirements. 
Doing this came with a fair amount of error fixing, debugging and refactorings in both parts of the application. 

Aside from the aforementioned, Bart also ensured the application was deployable by Dockerising the application. Furthermore, Bart handled the submissions of the different deliverables
and other Gitlab related issues. For example, fixing the problems we had when branches diverged or files were not syncing correctly. Lastly, Bart improved the visuals of the front-end, 
making it more usable and pleasant to interact with. 

Arnaud focused on the documentation of the API and the specification of the API. As well, Arnaud dealt with the error handling in the back end and ensuring the errors are displayed appropriately in the front end. 
Lastly, Arnaud wrote the report and delegated tasks throughout the project when applicable.  

Overall, we feel that we the teamwork throughout the project was good. Although some team members did more than others, we were all willing to help each other 
and put effort into the project. 

## Bonus Criteria
1. We increased the complexity of the endpoints throughout our API in a couple ways. For example, we allow for many more country data field to be input than stated in **Requirement 1.1**. Instead of only allowing GDP and Population we also allow emissions data, ISO Code, name and some others.
As well, the way we handled updating a country's data should be noted. The dropdown box allows for a nice way to select the country you want to update, displaying all it's current fields, not just the GDP and population data.
Like this you can change any field you want and submit the update request. Moreover, we allow for data searches before a given year, not just after. Lastly, we added an endpoint that calculates the population change of a continent over a given period of time. 
2. We have implemented an endpoint that makes use of a third party API. This endpoint can be found in the **/routers/country_routes.py** file. 
The third party API's documentation can be found on the following website: https://restcountries.com/. 
Our call to this API **gets** information about the country specified that is not in the provided database. Such as: the capital of the country, the country's currency, the languages spoken in the country and a variety of other things. 
3. Our application was made deployable by creating and properly configuring the **Dockerfile**. The **Docker instructions** section of the report helps to set this up. 
To meet the criteria of the bonus we create a separate image for the back-end and front-end of the application. When following the instructions the application is deployable and can be tested and used normally.
4. ### Once we have written the design part of the program this will be quick
5. ### Max could comment on this. 
