# @lentryd/web-client

A simple client for interacting with a web server. It automatically stores cookies and adds them to subsequent requests.

## Installation

```bash
npm install @lentryd/web-client
```

## Usage

```typescript
import WebClient from "@lentryd/web-client";

// Create a client with a base URL
const client = new WebClient("http://example.com");

// Specify that all requests will be sent to http://example.com/api
client.path.set("/api");

// Send a request to the /login endpoint (http://example.com/api/login)
const res = await client.post("/login", {
  body: {
    login: "admin",
    password: "admin",
  },
});

// Retrieve the token from the response
const token = res.json().then((data) => data.token);

// Add the token to the Authorization header (all future requests will be authenticated)
client.headers.set("Authorization", `Bearer ${token}`);

// Send a request to the /user endpoint (http://example.com/api/user)
const user = await client.get("/user");
```
