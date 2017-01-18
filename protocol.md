# Description

Request-Response protocol
HTTP 4.0 - JSON:ified

## Request:
```
{
	"type" : "<command>",
	"meta" : [ "key":"val" ],
	"data" : "<data>"
}
```

## Response:
```
{
	"result_code" : 200,
	"result_msg" : "<msg>",
	"meta" : ["key":"val"],
	"data" : "<data>"
}
```

## Note structure
Typical structure of a note. The MIME header does not need to exist.

```
Key: Value
Key: Value

<note content>
```

Typical MIME types examples:
```
Title: title of note
Category: cryptography
Tags: crypto,cbc,ecb
```

# API Definition

## Add Note
Add a newly created note to the system

### Request:
```
{
 	"command" : "add_note"
 	"meta" : [...]
 	"data" : "<valid note>"	
}
```

### Response
On a succesful insertion
```
{
	"result_code" : 200,
	"result_msg" : "Success.",
	"meta" : [...],
	"data" : ""
}
```

### Potential errors:
 * 500: ensure JSON is properly created.
 * 502: ensure note conforms to its standard.

## Fetch note
Fetch a note from the system. Specify the note to retrieve in the
body of the request. 

### Request
```
{
 	"command" : "fetch_note"
 	"meta" : [...]
 	"data" : <fetch-body>
}
```

Valid body values:

fetch the n-th previous note (-1 for previous)

> { "previous" : "-n" }

### Response
```
{
	"result_code" : 200,
	"result_msg" : "Success.",
	"meta" : [...],
	"data" : <note>
}
```

# Error messages

## 500 - Incorrect format
The received request was improperly formatted.

```
{
	"result_code" : 500,
	"result_msg" : "The request was not formatted properly.",
	"meta" : [...]
	"data" : ""
}
```

## 501 - Unrecognized Command
The specified commands does not exist.

```
{
	"result_code" : 501,
	"result_msg" : "Command '<command>' is not a recognized command.",
	"meta" : [...]
	"data" : ""
}
```

## 502 - Invalid request data
The data specified does in a request is not properly fomratted and incorrect.

```
{
	"result_code" : 502,
	"result_msg" : "Request data is not valid.",
	"meta" : [...]
	"data" : "<Specific error message>"
}
```

## 503 - Interal server error
Something unexpected occured on the server. See data for error message.

```
{
	"result_code" : 503,
	"result_msg" : "Internal Server Error",
	"meta" : [...]
	"data" : "<Specific error message>"
}
```
