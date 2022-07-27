from flask import Flask
import xmlrpc.client

app = Flask(__name__)
url = 'https://otlkm.odoo.com'
db = 'otlkm'
username = 'alvaromolinac@gmail.com'
password = 'G$hT74d$C2dmWf'

@app.route('/')
def hello_world():
    return 'Hello oddo-appi'

@app.route('/get_customers')
def get_customers():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    print(common.version())
    uid = common.authenticate(db, username, password, {})
    print(uid)
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    result = models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
    return str(result)