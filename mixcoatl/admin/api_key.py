import json

from mixcoatl.resource import Resource
from mixcoatl.decorators.lazy import lazy_property
from mixcoatl.decorators.validations import required_attrs

class ApiKey(Resource):
    """An API key is an access key and secret key that provide API access into enStratus."""
    
    path = 'admin/ApiKey'
    collection_name = 'apiKeys'
    primary_key = 'access_key'

    def __init__(self, access_key = None, *args, **kwargs):
        Resource.__init__(self)
        self.__access_key = access_key

    @property
    def access_key(self):
        """The primary identifier of the `ApiKey`. Same as `ES_ACCESS_KEY`"""
        return self.__access_key

    @lazy_property
    def account(self):
        """`dict` - The account with which this API key is associated."""
        return self.__account

    @lazy_property
    def activation(self):
        """`str` - The date and time when this key was activated."""
        return self.__activation

    @lazy_property
    def expiration(self):
        """`str` - The date and time when this API key should automatically be made inactivate."""
        return self.__expiration

    @expiration.setter
    def expiration(self, e):
        self.__expiration = e

    @lazy_property
    def customer(self):
        """`dict` - The customer to whom this API key belongs."""
        return self.__customer

    @lazy_property
    def customer_management_key(self):
        """`bool` - Identifies whether or not this key can be used across all customer accounts."""
        return self.__customer_management_key

    @lazy_property
    def description(self):
        """`str` - A user-friendly description of this API key."""
        return self.__description

    @description.setter
    def description(self, d):
        self.__description = d

    @lazy_property
    def name(self):
        """`str` - The user-friendly name used to identify the key."""
        return self.__name

    @name.setter
    def name(self, n):
        self.__name = n

    @lazy_property
    def secret_key(self):
        """`str` - The secret part of this API key."""
        return self.__secret_key

    @lazy_property
    def state(self):
        """`str` - The status of the key *(i.e. `ACTIVE`)*"""
        return self.__state

    @lazy_property
    def system_management_key(self):
        """`bool` - Identifies if the key can be used for enStratus system management functions"""
        return self.__system_management_key

    @lazy_property
    def user(self):
        """`dict` - The user associated with this API key. Account-level keys return `{'user_id': -1}`"""
        return self.__user

    @required_attrs(['description', 'name'])
    def create(self):
        """Call the API to generate an API key from the current instance of `ApiKey`"""

        payload = {'generateApiKey':[{'description':self.description, 'name':self.name}]}
        s = self.post(data=json.dumps(payload))
        if self.last_error is None:
            self.__access_key = s['apiKeys'][0]['accessKey']
            self.load()
        else:
            raise ApiKeyGenerationException(self.last_error)


    @classmethod
    def generate_api_key(obj, key_name, description, expiration=None):
        """Generates a new API key

        :param key_name: the name for the key
        :type key_name: str.
        :param description: the description for the key
        :type description: str.
        :param expiration: *unused for now*
        :type expiration: str.
        :returns: :class:`ApiKey`
        :raises: :class:`ApiKeyGenerationException`
        """
        a = obj()
        a.name = key_name
        a.description = description
        a.create()
        return a

    @classmethod
    def all(cls, **kwargs):
        """Get all api keys

        The keys used to make the original request determine
        the visible results.

        :param detail: The level of detail to return - `basic` or `extended`
        :type detail: str.
        :param account_id: Display all system keys belonging to `account_id`
        :type account_id: int.
        :param user_id: Display all keys belonging to `user_id`
        :type user_id: int.
        """
        r = Resource(cls.path)
        if 'detail' in kwargs:
            r.request_details = kwargs['detail']
        else:
            r.request_details = 'basic'
        
        if 'account_id' in kwargs:
            params = {'accountId': kwargs['account_id']}
        elif 'user_id' in kwargs:
            params = {'userId': kwargs['user_id']}
        else:
            params = {}

        c = r.get(params=params)
        if r.last_error is None:
            return [cls(i['accessKey']) for i in c[cls.collection_name]]
        else:
            return r.last_error

class ApiKeyException(BaseException): pass
class ApiKeyGenerationException(ApiKeyException): pass