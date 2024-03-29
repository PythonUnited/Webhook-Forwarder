# How to use this app

This webhook forwarder can be used to forward webhook payloads to multiple endpoints. 
This can be useful when developing and testing. For example when a payment provider has the 
limitation that only one webhook can be set for testing. Use an URL from this app to forward 
the webhook payload to both the test enviroment and development environment (using a local tunnel).

## Set-up in Django admin

First add a 'webhook identifier'. For example if this webhook will be used for the sandbox environment 
for Acme Payments, name it `Acme Payments (sandbox env)`. 

In the same form when adding or editing a 'webhook identifier', one or more URLs can be added to which 
the webhook payload should be forwarded. To test you could use a URL from https://webhook.site.

The name enetered earlier will be converted to a slug. The URL path will look like:

    /api/forwarder/1.0/webhooks/acme-payments-sandbox-env

Finally, add the URL to the service which fires the webhook. When a request is sent to the above, the 
app will forward the request to the URLs set in the webhook identifier.

## Open API docs caveat

Open API docs are available at `/api/docs`. However it is not possible to set a http payload via 
this interface. As Django Ninja is geared towards JSON and plain-text data schemas are not possible. 

## Local tunnel

A tunnelling solution can be used to set-up a local tunnel from your development env to this app. 

For example using local tunnel:

    npm install -g localtunnel

    lt --port 8000 --subdomain example-subdomain

Or any of the tunneling solutions listed here: https://github.com/anderspitman/awesome-tunneling