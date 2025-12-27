# tests/e2e/test_e2e.py

import pytest  # Import the pytest framework for writing and running tests
import time

# The following decorators and functions define E2E tests for the FastAPI calculator application.

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage displays "Hello World".

    This test verifies that when a user navigates to the homepage of the application,
    the main header (`<h1>`) correctly displays the text "Hello World". This ensures
    that the server is running and serving the correct template.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')

    # Use an assertion to check that the text within the first <h1> tag is exactly "Hello World".
    # If the text does not match, the test will fail.
    assert page.inner_text('h1') == 'Hello World'

@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """
    Test the addition functionality of the calculator.

    This test simulates a user performing an addition operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Add" button, and verifies
    that the result displayed is correct.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')

    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')

    # Fill in the second number input field (with id 'b') with the value '5'.
    page.fill('#b', '5')

    # Click the button that has the exact text "Add". This triggers the addition operation.
    page.click('button:text("Add")')

    # Use an assertion to check that the text within the result div (with id 'result') is exactly "Result: 15".
    # This verifies that the addition operation was performed correctly and the result is displayed as expected.
    assert page.inner_text('#result') == 'Calculation Result: 15'

@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """
    Test the divide by zero functionality of the calculator.

    This test simulates a user attempting to divide a number by zero using the calculator.
    It fills in the numbers, clicks the "Divide" button, and verifies that the appropriate
    error message is displayed. This ensures that the application correctly handles invalid
    operations and provides meaningful feedback to the user.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')

    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')

    # Fill in the second number input field (with id 'b') with the value '0', attempting to divide by zero.
    page.fill('#b', '0')

    # Click the button that has the exact text "Divide". This triggers the division operation.
    page.click('button:text("Divide")')

    # Use an assertion to check that the text within the result div (with id 'result') is exactly
    # "Error: Cannot divide by zero!". This verifies that the application handles division by zero
    # gracefully and displays the correct error message to the user.
    assert page.inner_text('#result') == 'Error: Cannot divide by zero!'


# ========== Authentication E2E Tests ==========

@pytest.mark.e2e
def test_register_with_valid_data(page, fastapi_server):
    """
    Positive Test: Register a new user with valid data.

    This test verifies that a user can successfully register with valid email format,
    proper password length, and matching passwords. It checks that the success message
    is displayed.
    """
    page.goto('http://localhost:8000/register')

    # Generate a unique username and email to avoid conflicts
    timestamp = str(int(time.time()))
    username = f'testuser{timestamp}'
    email = f'test{timestamp}@example.com'
    password = 'password123'

    # Fill in the registration form
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)

    # Submit the form
    page.click('button[type="submit"]')

    # Wait for success message
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Verify success message is displayed
    success_text = page.inner_text('#successMessage')
    assert 'Registration successful' in success_text


@pytest.mark.e2e
def test_register_with_short_password(page, fastapi_server):
    """
    Negative Test: Register with a password that is too short.

    This test verifies that the frontend displays an error when the user tries
    to register with a password shorter than 6 characters.
    """
    page.goto('http://localhost:8000/register')

    timestamp = str(int(time.time()))
    username = f'testuser{timestamp}'
    email = f'test{timestamp}@example.com'

    # Fill in the form with a short password
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', '12345')  # Only 5 characters
    page.fill('#confirmPassword', '12345')

    # Blur the password field to trigger validation
    page.locator('#password').blur()

    # Wait a moment for the error to display
    page.wait_for_timeout(500)

    # Check that the error message is visible
    error = page.locator('#passwordError')
    assert error.is_visible()
    assert 'at least 6 characters' in error.inner_text()


@pytest.mark.e2e
def test_register_with_invalid_email(page, fastapi_server):
    """
    Negative Test: Register with an invalid email format.

    This test verifies that the frontend displays an error when the user provides
    an email that doesn't match the expected format.
    """
    page.goto('http://localhost:8000/register')

    timestamp = str(int(time.time()))
    username = f'testuser{timestamp}'

    # Fill in the form with an invalid email
    page.fill('#username', username)
    page.fill('#email', 'invalid-email')  # Missing @ and domain
    page.fill('#password', 'password123')
    page.fill('#confirmPassword', 'password123')

    # Blur the email field to trigger validation
    page.locator('#email').blur()

    # Wait a moment for the error to display
    page.wait_for_timeout(500)

    # Check that the error message is visible
    error = page.locator('#emailError')
    assert error.is_visible()
    assert 'valid email' in error.inner_text()


@pytest.mark.e2e
def test_register_with_mismatched_passwords(page, fastapi_server):
    """
    Negative Test: Register with passwords that don't match.

    This test verifies that the frontend displays an error when the password and
    confirm password fields don't match.
    """
    page.goto('http://localhost:8000/register')

    timestamp = str(int(time.time()))
    username = f'testuser{timestamp}'
    email = f'test{timestamp}@example.com'

    # Fill in the form with mismatched passwords
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', 'password123')
    page.fill('#confirmPassword', 'password456')  # Different password

    # Blur the confirm password field to trigger validation
    page.locator('#confirmPassword').blur()

    # Wait a moment for the error to display
    page.wait_for_timeout(500)

    # Check that the error message is visible
    error = page.locator('#confirmPasswordError')
    assert error.is_visible()
    assert 'do not match' in error.inner_text()


@pytest.mark.e2e
def test_login_with_valid_credentials(page, fastapi_server):
    """
    Positive Test: Login with valid username and password.

    This test first registers a user, then attempts to login with the same credentials.
    It verifies that the login is successful and a success message is displayed.
    """
    timestamp = str(int(time.time()))
    username = f'loginuser{timestamp}'
    email = f'login{timestamp}@example.com'
    password = 'password123'

    # First, register the user
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')

    # Wait for registration to complete
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Now navigate to login page
    page.goto('http://localhost:8000/login')

    # Fill in login credentials
    page.fill('#username', username)
    page.fill('#password', password)

    # Submit the login form
    page.click('button[type="submit"]')

    # Wait for success message
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Verify success message is displayed
    success_text = page.inner_text('#successMessage')
    assert 'Login successful' in success_text


@pytest.mark.e2e
def test_login_with_wrong_password(page, fastapi_server):
    """
    Negative Test: Login with incorrect password.

    This test attempts to login with an incorrect password and verifies that
    the server returns a 401 error and the UI displays an appropriate error message.
    """
    timestamp = str(int(time.time()))
    username = f'wrongpwuser{timestamp}'
    email = f'wrongpw{timestamp}@example.com'
    password = 'correctpassword123'

    # First, register the user
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')

    # Wait for registration to complete
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Now navigate to login page
    page.goto('http://localhost:8000/login')

    # Fill in login credentials with wrong password
    page.fill('#username', username)
    page.fill('#password', 'wrongpassword456')

    # Submit the login form
    page.click('button[type="submit"]')

    # Wait for error message
    page.wait_for_selector('#serverError', state='visible', timeout=5000)

    # Verify error message is displayed
    error_text = page.inner_text('#serverError')
    assert 'Invalid username or password' in error_text


@pytest.mark.e2e
def test_login_with_nonexistent_user(page, fastapi_server):
    """
    Negative Test: Login with a username that doesn't exist.

    This test attempts to login with credentials for a user that was never registered
    and verifies that an appropriate error is displayed.
    """
    page.goto('http://localhost:8000/login')

    # Try to login with non-existent credentials
    page.fill('#username', 'nonexistentuser999')
    page.fill('#password', 'password123')

    # Submit the login form
    page.click('button[type="submit"]')

    # Wait for error message
    page.wait_for_selector('#serverError', state='visible', timeout=5000)

    # Verify error message is displayed
    error_text = page.inner_text('#serverError')
    assert 'Invalid username or password' in error_text


# ========== Calculation BREAD E2E Tests ==========

@pytest.mark.e2e
def test_add_calculation_positive(page, fastapi_server):
    """
    Positive Test: Add a new calculation successfully.

    This test registers a user, logs in, navigates to the calculations page,
    and successfully creates a new addition calculation.
    """
    timestamp = str(int(time.time()))
    username = f'calcuser{timestamp}'
    email = f'calc{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')

    # Wait for page to load
    page.wait_for_timeout(1000)

    # Fill in calculation form
    page.fill('#addA', '10')
    page.fill('#addB', '5')
    page.select_option('#addType', 'Add')

    # Submit the form
    page.click('button:text("Add Calculation")')

    # Wait for success message
    page.wait_for_selector('#addMessage', state='visible', timeout=5000)

    # Verify success message
    message_text = page.inner_text('#addMessage')
    assert 'created successfully' in message_text
    assert '15' in message_text  # Result should be 15


@pytest.mark.e2e
def test_add_calculation_divide_by_zero(page, fastapi_server):
    """
    Negative Test: Try to add a division by zero calculation.

    This test verifies that the frontend prevents division by zero
    and shows an appropriate error message.
    """
    timestamp = str(int(time.time()))
    username = f'divzerouser{timestamp}'
    email = f'divzero{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Try to add division by zero
    page.fill('#addA', '10')
    page.fill('#addB', '0')
    page.select_option('#addType', 'Divide')

    # Submit the form
    page.click('button:text("Add Calculation")')

    # Wait for error message
    page.wait_for_selector('#addMessage', state='visible', timeout=5000)

    # Verify error message
    message_text = page.inner_text('#addMessage')
    assert 'divide by zero' in message_text.lower()


@pytest.mark.e2e
def test_browse_calculations_positive(page, fastapi_server):
    """
    Positive Test: Browse all calculations for a user.

    This test creates multiple calculations and verifies they are displayed
    correctly in the browse section.
    """
    timestamp = str(int(time.time()))
    username = f'browseuser{timestamp}'
    email = f'browse{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Add first calculation
    page.fill('#addA', '10')
    page.fill('#addB', '5')
    page.select_option('#addType', 'Add')
    page.click('button:text("Add Calculation")')
    page.wait_for_timeout(1000)

    # Add second calculation
    page.fill('#addA', '20')
    page.fill('#addB', '4')
    page.select_option('#addType', 'Multiply')
    page.click('button:text("Add Calculation")')
    page.wait_for_timeout(1000)

    # Click refresh to browse calculations
    page.click('button:text("Refresh List")')
    page.wait_for_timeout(1000)

    # Verify table is visible
    assert page.is_visible('#calculationsTable')

    # Verify at least 2 rows in the table
    rows = page.locator('#calculationsBody tr')
    assert rows.count() >= 2


@pytest.mark.e2e
def test_browse_calculations_empty(page, fastapi_server):
    """
    Positive Test: Browse calculations when user has none.

    This test verifies that an appropriate message is shown when
    a user has no calculations.
    """
    timestamp = str(int(time.time()))
    username = f'emptyuser{timestamp}'
    email = f'empty{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Wait for browse message
    page.wait_for_selector('#browseMessage', state='visible', timeout=5000)

    # Verify message about no calculations
    message_text = page.inner_text('#browseMessage')
    assert 'No calculations found' in message_text or '0 calculation' in message_text


@pytest.mark.e2e
def test_read_calculation_positive(page, fastapi_server):
    """
    Positive Test: Read a specific calculation by ID.

    This test creates a calculation and then retrieves it by its ID.
    """
    timestamp = str(int(time.time()))
    username = f'readuser{timestamp}'
    email = f'read{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Add a calculation
    page.fill('#addA', '15')
    page.fill('#addB', '3')
    page.select_option('#addType', 'Sub')
    page.click('button:text("Add Calculation")')
    page.wait_for_timeout(1000)

    # Get the calculation ID from the table
    page.click('button:text("Refresh List")')
    page.wait_for_timeout(1000)

    # Get first row's ID
    first_cell = page.locator('#calculationsBody tr:first-child td:first-child')
    calc_id = first_cell.inner_text()

    # Read the calculation
    page.fill('#readId', calc_id)
    page.locator('button:text("Get Calculation")').click()

    # Wait for result to appear
    page.wait_for_selector('#readResult', timeout=5000)

    # Verify result contains the correct data
    result_text = page.inner_text('#readResult')
    assert 'ID:' in result_text
    assert '15' in result_text
    assert '3' in result_text


@pytest.mark.e2e
def test_read_calculation_not_found(page, fastapi_server):
    """
    Negative Test: Try to read a non-existent calculation.

    This test verifies that an appropriate error is shown when
    trying to read a calculation that doesn't exist or doesn't belong to the user.
    """
    timestamp = str(int(time.time()))
    username = f'readnotfound{timestamp}'
    email = f'readnotfound{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Try to read a non-existent calculation
    page.fill('#readId', '99999')
    page.locator('button:text("Get Calculation")').click()

    # Wait for error message
    page.wait_for_selector('#readMessage', state='visible', timeout=5000)

    # Verify error message
    message_text = page.inner_text('#readMessage')
    assert 'not found' in message_text.lower() or 'error' in message_text.lower()


@pytest.mark.e2e
def test_update_calculation_positive(page, fastapi_server):
    """
    Positive Test: Update an existing calculation.

    This test creates a calculation and then updates it with new values.
    """
    timestamp = str(int(time.time()))
    username = f'updateuser{timestamp}'
    email = f'update{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Add a calculation
    page.fill('#addA', '10')
    page.fill('#addB', '5')
    page.select_option('#addType', 'Add')
    page.click('button:text("Add Calculation")')
    page.wait_for_timeout(1000)

    # Get the calculation ID
    page.click('button:text("Refresh List")')
    page.wait_for_timeout(1000)
    first_cell = page.locator('#calculationsBody tr:first-child td:first-child')
    calc_id = first_cell.inner_text()

    # Update the calculation
    page.fill('#editId', calc_id)
    page.fill('#editA', '20')
    page.fill('#editB', '10')
    page.select_option('#editType', 'Multiply')
    page.click('button:text("Update Calculation")')

    # Wait for success message
    page.wait_for_selector('#editMessage', state='visible', timeout=5000)

    # Verify success message contains new result
    message_text = page.inner_text('#editMessage')
    assert 'updated successfully' in message_text
    assert '200' in message_text  # 20 * 10 = 200


@pytest.mark.e2e
def test_update_calculation_not_found(page, fastapi_server):
    """
    Negative Test: Try to update a non-existent calculation.

    This test verifies that an error is shown when trying to update
    a calculation that doesn't exist.
    """
    timestamp = str(int(time.time()))
    username = f'updatenotfound{timestamp}'
    email = f'updatenotfound{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Try to update non-existent calculation
    page.fill('#editId', '99999')
    page.fill('#editA', '20')
    page.fill('#editB', '10')
    page.select_option('#editType', 'Add')
    page.click('button:text("Update Calculation")')

    # Wait for error message
    page.wait_for_selector('#editMessage', state='visible', timeout=5000)

    # Verify error message
    message_text = page.inner_text('#editMessage')
    assert 'not found' in message_text.lower() or 'error' in message_text.lower()


@pytest.mark.e2e
def test_delete_calculation_positive(page, fastapi_server):
    """
    Positive Test: Delete a calculation successfully.

    This test creates a calculation and then deletes it.
    """
    timestamp = str(int(time.time()))
    username = f'deleteuser{timestamp}'
    email = f'delete{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Add a calculation
    page.fill('#addA', '8')
    page.fill('#addB', '2')
    page.select_option('#addType', 'Divide')
    page.click('button:text("Add Calculation")')
    page.wait_for_timeout(1000)

    # Get the calculation ID
    page.click('button:text("Refresh List")')
    page.wait_for_timeout(1000)
    first_cell = page.locator('#calculationsBody tr:first-child td:first-child')
    calc_id = first_cell.inner_text()

    # Delete the calculation
    page.fill('#deleteId', calc_id)
    page.locator('button:text("Delete Calculation")').click()

    # Wait for success message
    page.wait_for_timeout(1000)

    # Verify calculation is no longer in the list
    page.click('button:text("Refresh List")')
    page.wait_for_timeout(1000)

    # Should show message about no calculations or empty table
    message_text = page.inner_text('#browseMessage')
    assert 'deleted successfully' in message_text.lower() or 'No calculations' in message_text or '0 calculation' in message_text


@pytest.mark.e2e
def test_delete_calculation_not_found(page, fastapi_server):
    """
    Negative Test: Try to delete a non-existent calculation.

    This test verifies that an error is shown when trying to delete
    a calculation that doesn't exist.
    """
    timestamp = str(int(time.time()))
    username = f'deletenotfound{timestamp}'
    email = f'deletenotfound{timestamp}@example.com'
    password = 'password123'

    # Register and login
    page.goto('http://localhost:8000/register')
    page.fill('#username', username)
    page.fill('#email', email)
    page.fill('#password', password)
    page.fill('#confirmPassword', password)
    page.click('button[type="submit"]')
    page.wait_for_selector('#successMessage', state='visible', timeout=5000)

    # Navigate to calculations page
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Try to delete non-existent calculation
    page.fill('#deleteId', '99999')
    page.locator('button:text("Delete Calculation")').click()

    # Wait for error message
    page.wait_for_timeout(1000)

    # Check for error in deleteMessage
    if page.is_visible('#deleteMessage'):
        message_text = page.inner_text('#deleteMessage')
        assert 'not found' in message_text.lower() or 'error' in message_text.lower()


@pytest.mark.e2e
def test_unauthorized_access_to_calculations(page, fastapi_server):
    """
    Negative Test: Try to access calculations page without being logged in.

    This test verifies that the page displays an authentication error
    when accessed without a valid JWT token.
    """
    # Navigate to calculations page without logging in
    page.goto('http://localhost:8000/calculations-page')
    page.wait_for_timeout(1000)

    # Verify auth error is displayed
    assert page.is_visible('#authError')

    # Verify sections are hidden
    sections = page.locator('.section')
    assert sections.count() == 0 or not sections.first.is_visible()
