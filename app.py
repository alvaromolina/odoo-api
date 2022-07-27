from flask import Flask, request, json
import xmlrpc.client

app = Flask(__name__)
url = 'https://otlkm.odoo.com'
db = 'otlkm'
username = 'alvaromolinac@gmail.com'
password = 'G$hT74d$C2dmWf'

@app.route('/')
def hello_world():
    return 'Hello oddo-appi'

@app.route('/test')
def get_customers():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #result = models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
    result = models.execute_kw(db, uid, password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
    return str(result)


@app.route('/create', methods=['POST'])
def create():
    data = json.loads(request.data)
    print(data)
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return_id = models.execute_kw(db,uid, password, 'res.partner', 'create', [data['data']])
    return {'id' : return_id}