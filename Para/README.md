## Task 1: Basic Query Parameters
- Description: Create an endpoint that accepts multiple query parameters and returns them in a structured format.

### Details:

- Endpoint: /items/
Query Parameters: name, category, price
Return a JSON response with the query parameters in a dictionary format.

 

## Task 2: Query Parameters with Default Values and Optional Fields
- Description: Create an endpoint that uses query parameters with default values and optional fields.

### Details:

- Endpoint: /search/
Query Parameters: query, page, size
Return a JSON response with the search results and pagination info.

## Task 3: Request Body with Nested Pydantic Models
- Description: Create an endpoint that accepts a complex JSON request body with nested Pydantic models.

### Details:

- Endpoint: /users/
Request Body: Pydantic model with nested fields for address and profile
User: name, email, address: Address
Address: street, city, zip
Return the received data as JSON.

## Task 4: Query Parameters with String Validations
Description: Create an endpoint that validates query parameters using string validations that includes length and regex.

- Details:

Endpoint: /validate/
Query Parameters: username
Return a JSON response confirming the validation.

 

## Task 5: Combined Parameters and Validations
Description: Create an endpoint that combines path parameters, query parameters, and request body with validations.

### Details:

Endpoint: /reports/{report_id}
Path Parameter: report_id (must be positive)
Query Parameters: start_date, end_date
Request Body: Pydantic model with fields: title, content
Return a JSON response summarizing all the received data.
