# csv_deals
<h2>
1. What is it used for<br>
2. Installation<br>
3. How it works<br>
</h2>
<div style="background-color=white">
<h3>1. What is it used for</h3>
<h5>CSV converter is needed: <br></h5>
  - to upload your csv_file of "Gem deals" on the server. <br>
  - to convert it in Django ORM format and write data in the DB.<br>
  - to get some information from DB with custom filtering by API request.<br>

<h3>2. Installation</h3>
<h5>2.1 Clone the full repository:<br></h5>
- You need to copy URL_path of this repository by clicking green button "Code" or just in the browser URL-panel.<br>
- login to your local git in terminal, paste: <br>
<code>git clone URL_path</code><br>

<h5>2.2 Start docker container:<br></h5>
```
docker build --tag python-django .
docker run --publish 8000:8000 python-django
```
<h3>3. How it works</h3>
<h5>By HTML<br></h5>
.1 Go to your IP-address:8000/ <br>
Choose file, upload CSV file for analysis<br>
.2 Go back to your IP-address:8000/<br>
Click "Check Result"<br><br>

<h5>By API</h5><br>
.1 Upload csv file<br>
POST request: <br>
```html
endpoint: /api/v1/upload_csv
params: {'csv_file' = file}
```
.2 Get filtered data<br>
GET request: <br>
```html
endpoint: /api/v1/get_top_clients/{pk}/{pt}
params:
'pk': how many top clients we take into consideration (top_clients filter)
'pt': minimun amount of top clients to buy gem, we take this gem into consideration (gem_sell filter)
```
  *by default: pk=5, pt=2<br>
  /api/v1/get_top_clients/5/2/<br></div>