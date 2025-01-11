



### a) Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/himanjalsaha/Better_assignment
   ```
2. activate venv:
   ```bash
   venv/bin/activate
   ```
 3.  install required packages:
   ```bash
   pip install -r requirements.txt
```
4.make a .env file with:
 ```bash
   SECRET_KEY=your_secret_key  # Set this to a secret key for JWT
   ```



### b)design choices 
- used model controller services arcitecture
- made reusable functions following DRY principles
- made everything centrallised for better structure and easy accessibilty and mantainibilty
# auth
- use jwt tokens to perform token based auth
- Proper input validation and sanitization are implemented to ensure that only valid data
- this arcitecture abstracts datalayer(services) and business logic (controllers) making robust api



    


- **Authentication**:
  - Token-based authentication to secure API endpoints.
 

  ### Description of the key folders:

- `controllers`: Contains the logic to handle HTTP requests and responses.
- `models`: Defines the structure of data entities such as books and members.
- `routes`: Defines the API endpoints and ties everything together.
- `services`: Contains business logic for adding, updating, deleting, and retrieving books and members.
- `utils`: Helper functions, including token generation and validation for authentication.
- `.env`: Configuration for environment-specific variables (e.g., database connection strings).



