# NET322 Continuous Assessment Test II

## Task

You are required to implement a simple Python AsyncIO concurrent HTTP server.
_Lookout for **TODO** directive declarations in the source files_

### Milestones

Implement an HTTP server using Python's AsyncIO.

The server should be able to handle HTTP client requests that serve the HTML template resources found in the `templates` directory.

#### Expectation

1. When the server program is running,for instance on localhost:8085, should a Web browser fetch `http://localhost:8085/`, the server should respond with contents of the `index.html` template resource.
2. Similarly, if browser requests for `http://localhost:8085/register`, the server should respond with the contents of the `register.html` template resource.
3. Finally when the client (Web browser) is served registration template when calling `http://localhost:8085/register`, on submission of form shown on the page, the server should capture the form details and write the `username` and `email` to a TEXT file called `db.txt`. [HINT : Trap the POST method request].

   The username and email address fields should be written to the `db.txt` as a single line in this format.
    ```bash
        username email_address
    ``` 
Each entry should be written as a single line, any subsequent entires should be written on a separate line in the same `db.txt` file.
    
Achieving this objective fetches a total of 50 marks.



## Instructions
Refer to the source files provided.

**Submission of unoriginal work shall be penalized accordingly.**
````
