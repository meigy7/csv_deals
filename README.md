# csv_deals
<h3>
1. What is it used for
2. Installation
3. How it works
</h3>

<h5>1. What is it used for</h5>
CSV converter is needed: 
- to upload your csv_file of "Gem deals" on the server. 
- to convert it in Django ORM format and write data in the DB.
- to get some information from DB with custom filtering by API request.

<h5>2. Installation</h5>
2.1 Clone the full repository:
- You need to copy URL_path of this repository by clicking green button "Code" or just in the browser URL-panel.
- You need to open terminal, login to your local git, choose needed directory and paste: 
git clone URL_path

2.2 Start docker container:
docker build --tag python-django .
docker run --publish 8000:8000 python-django


<h5>3. How it works</h5>
By HTML
.1 Go to your IP-address:8000/
Choose file,  upload
.2 Go back to your IP-address:8000/
Click "Check Result"

By API
.1 Upload csv file
POST request: /api/v1/upload_csv
  params:{'csv_file' = file}
.2 Get filtered data
GET request: /api/v1/get_top_clients/{pk}/{pt}
  params:{'pk': how many top clients we take into consideration (top_clients filter)
          'pt': minimun amount of top clients to buy gem, we take this gem into consideration (gem_sell filter)}
  
  by default: pk=5, pt=2 
  /api/v1/get_top_clients/5/2/