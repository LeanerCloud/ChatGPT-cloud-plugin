# ChatGPT-cloud-plugin

ChatGPT plugin that will (one day) allow us to manage cloud resources from ChatGPT

## What we have so far

1. a local Flask web server that

- uses botocore to authenticate to AWS using a profile from `.aws/config`, for now hardcoded to `personal`
- serves a few static files required by the plugin documentation
- forwards requests received to AWS, authenticated with SigV4

1. the full EC2 OpenAPI YAML configuration taken from [APIs.guru](https://apis.guru)
1. a ChatGPT plugin configuration tying it all together

## Running it locally

- install the requirements, preferably in a Python virtualenv

```shell
pip install -r requirements.txt
```

- start the web server:

```shell
./aws_proxy.py NAME_OF_PROFILE_FROM_AWS_CONFIG
```

- test the web server:

```shell
 curl http://localhost:3000/.well-known/ai-plugin.json
{
    "schema_version": "v1",
    "name_for_human": "EC2",
    "name_for_model": "gpt4",
    "description_for_human": "Manage your AWS resources.",
[...]

$ curl -X GET "http://localhost:3000/?Action=DescribeSecurityGroups&Version=2016-11-15"

<?xml version="1.0" encoding="UTF-8"?>
<DescribeSecurityGroupsResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>22aba6e6-c226-487f-81d0-1cb0acc5aa04</requestId>
    <securityGroupInfo>
        <item>
[...]
```

## Current status

When attempting to load it locally into ChatGPT the browser tab seems to hang, probably the EC2 API definition is too big and we need to expose less functionality.

After a while you'll get a bunch of errors in the ChatGPT plugin loader. This is expected and what we've got so far.

## Contributing

Any contributions are welcome, hack away and send us pull requests if you make some progress.

## License

This software is licensed under the OSL-3 License.
