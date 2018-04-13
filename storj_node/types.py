from apistar import types, validators


class StorjNode(types.Type):
    address = validators.String(description='Host address')
    country = validators.String(description='Host geolocation country')
    city = validators.String(description='Host geolocation city')
    latitude = validators.Number(description='Host geolocation latitude')
    longitude = validators.Number(description='Host geolocation longitude')
    id = validators.String(description='Storj network id')
    last_seen = validators.DateTime(description='Last seen date', allow_null=True)
    last_timeout = validators.DateTime(description='Last timeout date', allow_null=True)
    port = validators.Integer(description='Node port')
    protocol = validators.String(description='Storj protocol used', allow_null=True)
    reputation = validators.Integer(description='Node reputation')
    response_time = validators.Number(description='Last response time')
    space_available = validators.Number(description='Space available of this node')
    timeout_rate = validators.Number(description='Timeout rate')
    user_agent = validators.String(description='Storj user agent', allow_null=True)
