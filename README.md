# Mixcoatl
Mixcoatl was the father of Quetzalcoatl. His name means "Cloud Serpent". Fitting for a Python library for the enStratus API.

## Word of warning
This repo is not feature complete. Preference is being given to API interactions that are most useful in conjuction with Fabric:

- Managing running instances
- Managing firewalls
- Interacting with Jobs
- Support for the above (budget codes, regions, datacenters)

Also the final API is being fleshed out based on how it is being used. Currently everything except `jobs` returns a specific object type - i.e. `Server`, `Firewall`, `FirewallRule`

All objects support lazy loading as well as an `.all()` class method.

# Usage notes
At a minimum, the following environment variables will need to be set:

- `ES_SECRET_KEY`
- `ES_ACCESS_KEY`

By default, api calls will be made against the enStratus production SaaS and API version `2012-06-15`. These can be overridden with the following variables:

- `ES_ENDPOINT`
- `ES_API_VERSION`

When overriding the endpoint, it should be in the form of:

`http[s]://api.endpoint.domain/enstratus/api/<api version>`

Note that setting both `ES_API_VERSION` and `ES_ENDPOINT` is not cumulative. If you wish to use a private endpoint, it must include the version in the url.

## Lazy loading
By default, any object you request by its id will not actually hit the endpoint. Only when you request the object in full or a specific attribute, will it actually make the API call. If the API call fails, the error will be returned to you. You can always check the object's `last_error` attribute to determine if it failed or not.

example:

```python
from mixcoatl.geography.cloud import Cloud
c = Cloud(1)
>>> # returns immediately
c.cloud_id
>>> 1
c.name
>>> # api call is made.
>>> u'Amazon Web Services'
```

## `.all()`
All objects should support a call to return all resources of that type. This will actually return a list of objects. Note that calling `.all()` actually deferences the objects so an API call will be made for each object:

example:

```python
from mixcoatl.geography.cloud import Cloud
c = Cloud.all()
>>> # Initial call made for all Clouds
c
>>> # Delay while each cloud object is dereferenced
c[0]
>>> {'status': 'ACTIVE', 'current_job': None, 'last_request': '<Response [200]>', 'name': 'Amazon Web Services', 'last_error': None, 'cloud_provider_name': 'Amazon', 'cloud_provider_console_url': 'http://aws.amazon.com', 'cloud_provider_logo_url': '/clouds/aws.gif', 'compute_endpoint': 'https://ec2.us-east-1.amazonaws.com,https://ec2.us-west-1.amazonaws.com,https://ec2.eu-west-1.amazonaws.com', 'compute_secret_key_label': 'AWS_SECRET_ACCESS_KEY', 'documentation_label': None, 'compute_delegate': 'org.dasein.cloud.aws.AWSCloud', 'path': 'geography/Cloud/1', 'compute_account_number_label': 'AWS_ACCOUNT_NUMBER', 'private_cloud': False}
type(c[0])
>>> mixcoatl.geography.cloud.Cloud
c[0].__class__.__name__
>>> 'Cloud'
```

## Pretty-printing
Every resource has a `.pprint()` function available which returns the prettyprinted object

example:
```python
from mixcoatl.geography.cloud import Cloud
c = Cloud(1)
c
c.pprint()
>>> # pretty print representation
```

# Other notes
In general, most resources should support read-only access. If you know the id of an resource, you can simply request the resource by name with the id as a parameter:

```python
from mixcoatl.infrastructure.server import Server
s = Server(12345)
s
>>> # server details returned
```

Importing resources generally follows the API directly i.e.:

`from mixcoatl.scope.resource import ResourceName`

so for firewalls:

```python
from mixcoatl.network.firewall import Firewall
f = Firewall(12345)
f
```

for servers:

```python
from mixcoatl.infrastucture.server import Server
s = Server(12345)
s
```

For specific examples per resource, see the [wiki](https://github.com/enStratus/mixcoatl/wiki)
