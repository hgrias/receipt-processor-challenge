# Development Notes

## Areas for Improvement

1. Data Persistence
   - implement a data store
2. Security
   - Add rate limiting
   - Input sanitization
   - Authentication/API Keys
3. Input Validation
    - Already using json schema for input validation, but could look to implement some other methods
4. Error Handling
    - database errors (if we implement a database connection)
    - `FileNotFoundError` if we implement a way to upload or download files
    - External API errors if we have to connect to them
5. Testing suite / CICD
   - Since I'm using python, implementing a pytest suite to include unit and integration tests would be ideal.
   - Add git hooks to run these tests whenever there is a push to a development branch or similar
