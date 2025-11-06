## Explanation

This is a vulnerable web server using the Flask framework in python that connects to a PostgreSQL database. The way the webapp interacts with the db is really bad coded, and is vulnerable to SQL Injection.

## Steps to set up

```bash
git clone https://github.com/daemoncibsec/Vulnerable_Webpage.git
cd Vulnerable_Webpage
pip install -r requirements.txt
```

After installing this, you need to change some values on the script (vulnerable.py file). Being more specific, you need to search for this four strings in the script and change them to whatever configuration you're using:

- YOUR_SERVER_IP_ADDRESS
- YOUR_POSTGRES_DATABASE
- YOUR_DB_USER
- YOUR_DB_USER_PASSWORD

## Usage/Examples

- To start the server:

```bash
python3 vulnerable.py
```

*Also, make sure the PostgreSQL Database is working, otherwise you won't get passed the login screen.*

## Authors

- [@daemoncibsec](https://www.github.com/daemoncibsec)
