from flask import Flask, request, json
import xmlrpc.client

app = Flask(__name__)
url = 'https://nowmobile.odoo.com'
db = 'nowmobile'
username = 'kabro77@gmail.com'
password = '@fqzz5tiQc6WA2'
#8fb9ce842facbf92acb043fc8cebc592d57406fe

@app.route('/')
def hello_world():
    return 'Hello oddo-appi'

@app.route('/test')
def get_customers():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #result = models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
    result = models.execute_kw(db, uid, password, 'sale.subscription', 'search_read', [[['id', '=', 19]]], {'fields': ['stage_id']})
    return result[0]


@app.route('/create', methods=['POST'])
def create():
    data = json.loads(request.data)
    print(data)
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return_id = models.execute_kw(db,uid, password, data['model'], 'create', [data['data']])
    return {'id' : return_id}

@app.route('/get_client/<client_id>')
def get_client(client_id: int):
    print(client_id)
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    ids = [client_id]
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    result = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['id', '=', client_id]]], {'fields': ['name', 'email', 'phone', 'street', 'zip']})
    if len(result) > 0:
        result[0]['iccd'] = '891004234814'+str(client_id)+'5936F'
        result[0]['imsi'] = '3134600000000'+str(client_id)
    return result[0] if len(result) > 0 else {}

@app.route('/subscription', methods=['POST'])
def subscription():
    data = json.loads(request.data)
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    line_vals = {
        'product_id': 1,
        'uom_id': 1,
        'price_unit': 100,
    }
    order_vals = {
        'partner_id': int(data['client_id']),
        'template_id': 1,
        'stage_id' : 1,
        'recurring_invoice_line_ids' : [(0, 0, line_vals)],
    }
    subscription_id = models.execute_kw(db, uid, password, 'sale.subscription', 'create', [order_vals])
    return {"subscription_id" : subscription_id}


@app.route('/change_number', methods=['POST'])
def change_number():
    data = json.loads(request.data)
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    result = models.execute_kw(db, uid, password, 'res.partner', 'write', [[data['client_id']], {'phone': data['msisdn'], 'mobile': data['msisdn']}])
    return {'id' : data['client_id']}


@app.route('/activate_subscription', methods=['POST'])
def activate_subscription():
    data = json.loads(request.data)
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    [subscription_id] = models.execute_kw(db, uid, password, 'sale.subscription', 'search', [[['partner_id', '=', data['client_id']]]], {'limit': 1})
    models.execute_kw(db, uid, password, 'sale.subscription', 'write', [[subscription_id], {'stage_id': 2}])
    #models.execute_kw(db, uid, password, 'res.partner', 'write', [[data['client_id']], {'phone': data['msisdn'], 'mobile': data['msisdn']}])
    return {'subscription_id' :subscription_id}

