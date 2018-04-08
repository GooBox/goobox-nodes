from apistar import typesystem


class StorjNode(typesystem.Object):
    description = 'Storj node object'
    properties = {
        'address': typesystem.string(description='Host address'),
        'country': typesystem.string(description='Host geolocation country'),
        'city': typesystem.string(description='Host geolocation city'),
        'latitude': typesystem.string(description='Host geolocation latitude'),
        'longitude': typesystem.string(description='Host geolocation longitude'),
        'id': typesystem.string(description='Storj network id'),
        'last_seen': typesystem.string(description='Last seen date'),
        'last_timeout': typesystem.string(description='Last timeout date'),
        'port': typesystem.integer(description='Node port'),
        'protocol': typesystem.string(description='Storj protocol used'),
        'reputation': typesystem.integer(description='Node reputation'),
        'response_time': typesystem.number(description='Last response time'),
        'space_available': typesystem.number(description='Space available of this node'),
        'timeout_rate': typesystem.number(description='Timeout rate'),
        'user_agent': typesystem.string(description='Storj user agent'),
    }
