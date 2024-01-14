# Getting started

## Explanation of Requirement 1

### Requirement 1.1
The following list outlines where to go in the front-end application for the different parts of this requirement:
- **Retrieve**: Fetch Country Data section.
    - If there is no year input, then all available data for the country will be displayed. If there is a year input, the **timeframe** decides what data is displayed.  
    - The **timeframe** works as follows. You can input:
      - before: Gets the relevant country data **before** the specified year
      - equal: Gets the relevant country data **for** the specified year
      - after: Gets the relevant country data **including and after** the specified year
    - The **timeframe** value defaults to **after** if it is not specified. This applies to all places where a **timeframe** is prompted in the front-end application. 

- **Create**: Create Country Data section. 
- **Delete**: Delete Country Data section.
- **Update**: Update Country Data section.

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
