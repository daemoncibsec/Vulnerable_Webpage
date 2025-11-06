from flask import Flask, render_template, redirect, request, session, flash, url_for
import psycopg2
import psycopg2.extras
from psycopg2 import OperationalError, sql

app = Flask(__name__)
app.secret_key = "gSif427fQXGFA1Ss4B56EtXiT+QxjlpabNzEYOhI+oNT93/6hRi0IkgPMCStRfhe"

host = "YOUR_SERVER_IP_ADDRESS"
db = "YOUR_POSTGRES_DATABASE"

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash("Usuario y contraseña obligatorios")
        return redirect(url_for('index'))
    try:
        conn = psycopg2.connect(
            dbname=db,
            user='YOUR_DB_USER',
            password='YOUR_DB_USER_PASSWORD',
            host=host,
            connect_timeout=5
        )
        conn.close()
    except OperationalError as e:
        flash(f"Error de conexión: {e}")
        return redirect(url_for('index'))
    session['db_user'] = username
    session['db_password'] = password 
    session['authenticated'] = True
    return redirect(url_for('tables'))

@app.route('/tables', methods=['GET'])
def tables():
    if not session.get('authenticated'):
        flash("Debes iniciar sesión primero")
        return redirect(url_for('index'))

    username = session.get('db_user')
    password = session.get('db_password')
    try:
        conn = psycopg2.connect(
            dbname=db,
            user='YOUR_DB_USER',
            password='YOUR_DB_USER_PASSWORD',
            host=host
        )
    except OperationalError as e:
        flash(f"Error al conectar con la base de datos: {e}")
        return redirect(url_for('index'))
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(f"SELECT schemaname, tablename, tableowner FROM pg_catalog.pg_tables WHERE tableowner = '{username}' ORDER BY schemaname, tablename;",)
        rows = cur.fetchall()
    except Exception as e:
        flash(f"Error ejecutando la consulta: {e}")
        rows = []
    finally:
        cur.close()
        conn.close()
    tables = [{"schema": r["schemaname"], "name": r["tablename"], "owner": r["tableowner"]} for r in rows]
    return render_template('tables.html', tables=tables, user=username)

@app.route('/table/<schema>/<table>', methods=['GET'])
def view_table(schema, table):
    if not session.get('authenticated'):
        flash("Debes iniciar sesión primero")
        return redirect(url_for('index'))
    username = session.get('db_user')
    password = session.get('db_password')
    try:
        conn = psycopg2.connect(
            dbname=db,
            user='YOUR_DB_USER',
            password='YOUR_DB_USER_PASSWORD',
            host=host
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f'SELECT * FROM "{table}";')
        rows = cur.fetchall()
        columns = list(rows[0].keys()) if rows else []
    except Exception as e:
        flash(f"No se pudo leer la tabla: {e}")
        rows = []
        columns = []
    finally:
        cur.close()
        conn.close()
    return render_template('table_view.html', table=table, schema=schema, rows=rows, columns=columns)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

