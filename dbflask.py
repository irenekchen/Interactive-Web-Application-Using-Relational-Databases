import json

from flask import Flask
from flask import request

import dbaccess


app = Flask(__name__)

#GET: /api/<resource>[query_expression],[&field_expression]
@app.route('/api/<resource>', methods=["GET"])
def get_base_resource(resource):
	args = request.args

	query_expression = dict(args)
	if "fields" in args.keys():
		field_expression = args['fields']
		del query_expression['fields']
	else:
		field_expression = None
	list_key_value = [ [k,v] for k, v in query_expression.items() ]

	query = []
	for k, v in list_key_value:
		dic = dict()
		dic["column"] = k
		dic["value"] = v[0]
		query.append(dic)

	result = dbaccess.get_by_template(resource, field_expression, query)
	return result.to_json(orient='records')

#POST: /api/<resource> creates (inserts) a new sub-resource (row) in the containing resource (table).
@app.route('/api/<resource>', methods=["POST"])
def add_base_resource(resource):
	if (request.is_json):
		new_resource = request.get_json()
		dbaccess.insert(resource, new_resource)
		return "POST request completed."
	return "NOT FOUND", 404

#GET: /api/<resource>/<primary_key>[?fields_expression] returns the identified resource (row).
@app.route('/api/<resource>/<primary_key>', methods=["GET"])
def get_specific_resource(resource, primary_key):
	table_primary_key = dbaccess.get_primary_key(resource)

	print(table_primary_key)
	query = []
	dic = dict()
	dic["column"] = table_primary_key[0]
	dic["value"] = primary_key
	query.append(dic)

	args = request.args

	if "fields" in args.keys():
		field_expression = args['fields']
	else:
		field_expression = None

	result = dbaccess.get_by_template(resource, field_expression, query)
	return result.to_json(orient='records')

#PUT: /api/<resource>/<primary_key> updates the resource (row).
@app.route('/api/<resource>/<primary_key>', methods=["PUT"])
def put_specific_resource(resource, primary_key):
	table_primary_key = dbaccess.get_primary_key(resource)

	print(table_primary_key)
	query = []
	dic = dict()
	dic["column"] = table_primary_key[0]
	dic["value"] = primary_key
	query.append(dic)

	args = request.args

	if "fields" in args.keys():
		field_expression = args['fields']
	else:
		field_expression = None

	dbaccess.delete(resource, query)

	if (request.is_json):
		new_resource = request.get_json()
		dbaccess.insert(resource, new_resource)
	return "PUT request completed."

#DELETE: /api/<resource>/<primary_key> deletes the identified resource.
@app.route('/api/<resource>/<primary_key>', methods=["DELETE"])
def delete_specific_resource(resource, primary_key):
	table_primary_key = dbaccess.get_primary_key(resource)

	query = []
	dic = dict()
	dic["column"] = table_primary_key[0]
	dic["value"] = primary_key
	query.append(dic)

	args = request.args

	if "fields" in args.keys():
		field_expression = args['fields']
	else:
		field_expression = None

	dbaccess.delete(resource, query)

	return "DELETE request sent."

#GET: /api/<resource>/<primary_key>/<related_resource>[query_expression][fields_expression] returns the set of resource related to a specific resource by a relationship, and which match a query.
@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=["GET"])
def get_dependent_resource(resource, primary_key, related_resource):

	#first retrieve the first primary key param
	resource_primary_key = dbaccess.get_primary_key(resource)
	query = []
	dic = dict()
	dic["column"] = resource_primary_key[0]
	dic["value"] = primary_key
	# list of size one of primary key mapping to value
	query.append(dic)

	#now retrieve and create the rest of the template
	args = request.args
	query_expression = dict(args)
	if "fields" in args.keys():
		field_expression = args['fields']
		del query_expression['fields']
	else:
		field_expression = None
	list_key_value = [ [k,v] for k, v in query_expression.items() ]

	for k, v in list_key_value:
		dic = dict()
		dic["column"] = k
		dic["value"] = v[0]
		query.append(dic)

	result = dbaccess.get_by_template(related_resource, field_expression, query)
	return result.to_json(orient='records')

#POST: /api/<resource>/<primary_key>/<related_resource>  creates a new related resource.
@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=["POST"])
def add_dependent_resource(resource, primary_key, related_resource):

	#first retrieve the first primary key param
	resource_primary_key = dbaccess.get_primary_key(resource)
	query = []
	dic = dict()
	dic["column"] = resource_primary_key[0]
	dic["value"] = primary_key
	# list of size one of primary key mapping to value
	query.append(dic)

	#now retrieve and create the rest of the template
	result = dbaccess.get_by_template(resource, None, query)
	if len(result) != 0:
		if (request.is_json):
			new_resource = request.get_json()
			new_resource[resource_primary_key[0]] = primary_key
			dbaccess.insert(related_resource, new_resource)
			return "POST request completed."
	return "NOT FOUND", 404


if __name__ == '__main__':
    app.run()