# 🧩 Climate Visualization Pair Coder
## prerequis
Install :
 - PostgreSQL
 - Python 3


 Install the dependenies :
-  pip install -r Codebook/backend/requirements.txt

## Postgresql 

If a PostgreSQL database backup is provided, restore the backup using PostgreSQL/pgAdmin.
Else 
Create a new PostgreSQL database, then execute the SQL script provided with the project:
Codebook/database.sql
The SQL script creates the required database tables and constraints.



Configuration of postgreSQL connection
Open Codebook/backend/app.py

The following parameters must be adapted to the local PostgreSQL installation:

DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "climate_visu",
    "user":"postgres",
    "password":"postgres",
}

## Start Flask Backend

Open a terminal in the project directory and run:

python backend/app.py

The backend should start on:

http://127.0.0.1:5000

You can check the database connection by opening:

http://127.0.0.1:5000/api/health

A successful connection should return:

{
  "status": "ok",
  "database": "connected"
}



## 🧭 How to Use
 Open `Codebook/index.html` in a browser.

## Select coder name
Select your name in the Coder section
Each coder has their own coding results in PostgreSQL.




Media options: `bbc`, `guardian`, `nytimes`.

3. Import the outlet CSV:
   `output/<media>/<media>_images_dataviz_dedup.csv`
4. Import the matching image folder:
   `output/<media>/<media>_images/<media>_images_dataviz_dedup/`




5. Select a media image row. Article metadata is filled from the CSV.
6. Upload the original scientific figure.
7. Complete pair metadata and transformation coding.
8. Click `Save and next`.


## Local files

The application still uses local files for the media data and images.
PostgreSQL does not store the image files themselves.

If images were coded during another session by a coder, it will not currently be possible to export the results.