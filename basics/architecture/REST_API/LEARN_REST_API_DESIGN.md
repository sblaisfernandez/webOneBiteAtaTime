# RESTful API

In 2000, Roy Fielding, proposed an architectural approach for web-services know as
**Representational State Transfer (REST)**. REST is not tied to HTTP. These API's provide way to identify a resource by its URI, which can be used to transfer a representation or a resource's current state over HTTP.

REST API should be language agnostic.

[HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) or the Hypermedia As The Engine Of Application State is the important feature of every scalable and flexible REST API.

## ROY Fielding 6 constraints

- **Uniform Interface**: The client and the server should by decouple and evolve independently.

- **Stateless:** The server should not save any states between different requests. The state of the session is exclusively left to the responsibility of the client. **All REST interactions are stateless. That is, each request contains all of the information necessary for a connector to understand the request, independent of any requests that may have preceded it.**

- **Cacheable:** The Client should be able to store responses in a cache for the greater performance.

- **Client-server** architecture: Client in the web browser and the Server on the back-end.

- **Layered System**: The client can't tell whether it is connected directly to the end server, or to an intermediary. INtermediary servers can improve system scalability by enabling load-balancing and by providing shared caches. layers may also enforce security policies.

- **Code on** Demand (optional): Server are able to temporarily extend client fonctionnality by transfering logic.Could be passing JS components.

### API Design

- Resources: A resource is an object that's is referenced by it self.

- Collection: A collection is a group of resource.

- HTTP method: HTTP verbs (POST/GET/PUT/DELETE/PATCH)

Use a envelope to pass the data, it will allow to add more fields in the futur.

```json
{
  "user": {
    "id": 123,
    "firstName": "Sebastien",
    "lastName": "Blais"
  }
} <-- envelope
```

Treat the resource like a noun and HTTP methods as verbs.

`GET /blogposts` get all blogposts

`GET /blogposts/12` get the blogpost with the id 12

`POST /blogposts/` add new blogpost

`DELETE /blogposts/12` remove blogposts at id 12

`GET /authors/3/blogposts` get all the blogpost of the author with id 3

`PUT /blogposts/12` create and idempotent update (send all the fields required)

**idempotent requests** Multiple requests will have the same effects.

`PATCH /blogposts/12` partial change

## Actions

- Sorting: To sort a list of item in a list
    `GET /blogposts?sort=date`

- Filtering: To filter a list of item in a list
    `GET /blogposts?language=french&location=canada`

- Searching: To search a value in the database

    `GET /compagnies?search=TheNewWeb`

- Pagination: To GET a slice of the list by page
    `GET /blogposts?page=23`

## Rate limiting

`X-Rate-Limit-Limit`: The number of allowed requests in the current period

`X-Rate-Limit-Remaining`: The number of remaining requests in the current period

`X-Rate-Limit-Reset`: The number of seconds left in the current period

## Status Codes

Use the HTTP Status Codes to return feed back to the user.

- 200 OK
- 201 Created
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Unprocessable Entity
- 429 Too Many Request
- 500 Internal Server Error

## REST API Versioning

A well desing RESTful API include versining.

It can be in the URI as:
`GET https://api.example.com/v1.0.0/authors/2/blogposts/13`

Or passing into the header with:

GET
`X-API-Version: 1.0.0`
`Content-Type: application/json`

## Caching

## Error Handling

**Don't leave the user hanging with our proper error response**

TWITTER

request
`GET https://api.twitter.com/1.1/account/settings.json`

response

```json
{
  "errors":[
    {
      "code":215,
      "message":"Bad Authentication data."
    }
  ]
}
```

FACEBOOK

request
`GET https://graph.facebook.com/me/photos`

response

```json
{
  "error": {
    "message": "An active access token must be used to query information about the current user.",
      "type": "OAuthException",
      "code": 2500,
      "fbtrace_id": "DzkTMkgIA7V"
   }
}
```

## Documentation

**API is a good has is documentation**

[Twilio](https://www.twilio.com/docs/api/rest/)
[Google Map](https://developers.google.com/maps/documentation/)
[PARSE](https://docs.parseplatform.org/rest/guide/#your-configuration)

## References

[Learn REST](https://www.restapitutorial.com/)

[Best pratice restful api](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)

[API Design by Microsoft](https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design)

[API best practices](https://code-maze.com/top-rest-api-best-practices/)

[RESTful API tutorial](https://restfulapi.net/rest-api-design-tutorial-with-example/)
