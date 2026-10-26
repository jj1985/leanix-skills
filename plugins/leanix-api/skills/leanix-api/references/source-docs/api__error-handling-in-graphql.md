<!-- Source: https://help.sap.com/docs/leanix/ea/error-handling-in-graphql -->
<!-- Captured: 2026-10-26 -->
<!-- Product: SAP LeanIX -->

# Error Handling in GraphQL

Learn how error handling in GraphQL works and how to manage GraphQL
errors.

## Overview

GraphQL is a powerful query language for APIs that provides a flexible and efficient
approach to handling data. However, error handling in GraphQL differs from error
handling in traditional REST APIs, particularly regarding the use of HTTP status
codes.

Unlike REST APIs, which use HTTP status codes to indicate the success or failure of a
request, GraphQL always responds with a `200 OK` HTTP status code, even when
an error occurs. This happens because GraphQL requests can result in partial success and
partial failure at the same time. For example, when a GraphQL query is used to request
multiple fields, some fields may return data successfully, while other fields may return an
error.

In GraphQL, operational errors are treated as data, not as network errors. Therefore,
the HTTP status code does not reflect the success or failure of the operation.
Instead, the success or failure is communicated in the response body.

## Error Handling in SAP LeanIX GraphQL

When an error occurs in SAP LeanIX
GraphQL, the response includes an `errors` array in the JSON payload.
Each error object in the array contains a `message` field that
describes the error. It may also contain a `locations` field that
provides additional information.

Example GraphQL error response:

```json
{
  "data": null,
  "errors": [
    {
      "message": "Validation error of type FieldUndefined: Field nonExistenField is undefined",
      "locations": [
        {
          "line": 6,
          "column": 9
        }
      ]
    }
  ]
}
```

## Error Handling for Batch Mutations

When multiple mutations are included in a request and at least one mutation is
invalid, none of the mutations are executed. The `data` and
`errors` attributes provide details about the failed
mutation.

In the example request below, the mutation `m2` for updating a fact
sheet includes an invalid field: `descriptio`.

Example request:

```
mutation {
  m1: updateFactSheet(
    id: "d9506c79-5d4e-4661-9297-b3b84bd17b79"
    patches: [{ op: replace, path: "/description", value: "first description" }]
  ) {
    factSheet {
      id
      description
    }
  }
  m2: updateFactSheet(
    id: "3b2f5b03-8cff-4aa1-a619-38aa7e90d456"
    patches: [
      { op: replace, path: "/descriptio", value: "invalid field description" }
    ]
  ) {
    factSheet {
      id
      description
    }
  }
  m3: updateFactSheet(
    id: "351ee5ff-c851-48c5-92e6-3d373c6483ce"
    patches: [
      { op: replace, path: "/description", value: "third description" }
    ]
  ) {
    factSheet {
      id
      description
    }
  }
}
```

In the response, the `data` attribute returns `null`.
The `errors` attribute provides details about the failed mutation. An
error message indicates that the entire request hasn't been executed and none of the
mutations have been applied.

Example response:

```json
{
  "data" : null,
  "errors" : [ {
    "message" : "The path '/descriptio' is invalid in FactSheet schema Application.",
    "path" : [ "m2" ],
    "extensions" : {
      "errorType" : "BUSINESS_LOGIC"
    }
  }, {
    "message" : "Error in Request. Transaction is rolled back!",
    "path" : [ ],
    "extensions" : {
      "errorType" : "BUSINESS_LOGIC"
    }
  } ]
}
```

## Handling Errors in Your Application

When working with the SAP LeanIX
GraphQL API, ensure to design your application to handle errors in the response
body, not based on the HTTP status code. Here are some steps you can follow:

1. Check for the `errors` field in the response: After making a
GraphQL request, always check if the `errors` field is
present in the response. If it's present, it means one or more errors
occurred.

2. Parse the error message: Each error object within the
`errors` array includes a `message` field.
This field usually contains a description that can help you understand the
nature of the error that occurred. Please note that the clarity and
comprehensibility of these messages can vary, and they may not always
provide a complete picture of the issue. We recommend using error messages
as a starting point for troubleshooting, keeping in mind that they don't
provide a definitive diagnosis of the problem.

3. View the error location: The `locations` field in the
GraphQL error response is designed to provide specific details about where
in the query or mutation the error occurred. It contains an array of
objects, each with the `line` and `column`
properties. The `line` property indicates the line number in
the query or mutation where the error was encountered. Similarly, the
`column` property specifies the character position within
that line where the error was detected. In the provided error response, the
`locations` field indicates that the error was found on
line 6 in column 9 of the query or mutation.

Remember that the absence of the `errors` field in the response
indicates that the operation was successful.
