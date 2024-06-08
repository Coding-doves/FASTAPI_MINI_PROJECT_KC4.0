1. Simple Blog Post Creation:
Create an API endpoint that accepts a POST request with form data for blog post title, content, and author (optional).
Validate the data using Pydantic models (ensure title and content are present, author can be optional).
Save the blog post data and return a 201 Created response with a response model containing the created post details (ID, title, content, author).
If validation fails, return a 400 Bad Request response with an error model containing specific details about the invalid data.

 

2. User Profile Update with Image Upload:
Design an API endpoint that allows users to update their profile information (name, email) and upload an avatar image.
Use form data for name and email, and UploadFile for the image.
Validate the received data (e.g., name length, email format).
Perform image size and format validation (e.g., JPEG, PNG).
Update user information and save the uploaded image.
Return a 200 OK response with a response model containing the updated user details (including image URL).
Use a 400 Bad Request response with an error model for invalid data or image format.

 

3. Product Search with Pagination and Filtering:
Develop an API endpoint that accepts a GET request with query parameters for product search (search term, category, price range).
Allow optional pagination parameters (page number, page size).
Validate and sanitize search terms on the server-side (prevent SQL injection).
Perform product search based on criteria and pagination.
Return a 200 OK response with a response model containing a list of matching products and pagination information (total results, current page, etc.).
Use a 400 Bad Request response with an error model for invalid parameters or query syntax errors.

 

4. Secure Registration with OTP Verification:
Implement an API endpoint for user registration using a POST request with form data for email, password, and optional phone number.
Generate a secure password hash on the server-side.
Send an OTP (One-Time Password) to the user's email or phone (using an external service).
Return a 201 Created response with a response model containing a user ID and instructions to verify the OTP.
Create a separate endpoint for OTP verification using a POST request with form data for OTP code.
Validate the OTP and activate the user account.
Return a 200 OK response with a success model or a 400 Bad Request response with an error model for invalid OTP or registration errors.

 

5. E-commerce Shopping Cart Management:
Build API endpoints for managing a shopping cart:
Adding items to the cart (POST with form data for product ID and quantity).
Removing items from the cart (DELETE with query parameter for product ID).
Updating item quantities in the cart (PUT with form data for product ID and updated quantity).
Use Pydantic models to represent cart items and validate data.
Handle cart item limits and stock availability.
Return a 200 OK response with a success model or a 400 Bad Request response with an error model for invalid product IDs or quantity updates.
