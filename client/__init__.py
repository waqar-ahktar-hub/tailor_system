"""A django-rest-framework based client CRUD application.

This is a django rest framework based application which does
the following tasks.
1. Create a model for Client having following fields
    1. name (string)
    2. age (int)
    3. address (string)
    4. phone (string)
    5. email (string)
    g. gender (string -> M/F/Ot)
2. Provide CRUD functionality for client through rest apis.

The CRUD functionality provided can be used via:
1. GET Clients list
    GET http://host:port/client/clients/
2. Add Client
    POST http://host:port/client/clients/
3. GET Client by id
    GET http://host:port/client/clients/<id>/
4. DELETE Client by id
    DELETE http://host:port/client/clients/<id>/
5. Update Client by id
    PUT http://host:port/client/clients/<id>/
"""
