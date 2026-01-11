import { test, expect } from '@playwright/test';

// Test the Phase 2 Full-Stack Todo Application
test.describe('Phase 2 Todo Application', () => {
  const userEmail = `testuser_${Date.now()}@example.com`;
  const userPassword = 'TestPassword123!';

  test.beforeEach(async ({ page }) => {
    // Set base URL for the frontend
    await page.goto('http://localhost:3000');
  });

  test('should allow user signup, login, and task management', async ({ page }) => {
    // 1. Navigate to signup page
    await page.getByText('Create one here').click(); // Link to signup from login page

    // 2. Fill in signup form
    await page.locator('input[type="email"]').fill(userEmail);
    await page.locator('input[type="password"]').fill(userPassword);

    // 3. Submit signup form
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // 4. Verify successful signup and redirect to dashboard
    await expect(page).toHaveURL('http://localhost:3000/dashboard');

    // 5. Verify user is logged in by checking for dashboard elements
    await expect(page.getByText('My Tasks')).toBeVisible();

    // 6. Create a new task
    await page.locator('input[placeholder="What needs to be done?"]').fill('Test Task 1');
    await page.locator('textarea[placeholder="Add any additional details..."]').fill('This is a test task description');
    await page.getByRole('button', { name: 'Create Task' }).click();

    // 7. Verify task appears in the task list
    await expect(page.getByText('Test Task 1')).toBeVisible();
    await expect(page.getByText('This is a test task description')).toBeVisible();

    // 8. Create another task
    await page.locator('input[placeholder="What needs to be done?"]').fill('Test Task 2');
    await page.locator('textarea[placeholder="Add any additional details..."]').fill('Second test task');
    await page.getByRole('button', { name: 'Create Task' }).click();

    // 9. Verify both tasks appear
    await expect(page.getByText('Test Task 1')).toBeVisible();
    await expect(page.getByText('Test Task 2')).toBeVisible();

    // 10. Toggle first task as complete
    const firstDoneButton = page.locator('.space-y-3').getByRole('button', { name: 'Done' }).first();
    await firstDoneButton.click();

    // 11. Verify task is marked as complete
    await expect(page.locator('h3').filter({ hasText: 'Test Task 1' }).first()).toHaveClass(/line-through/);

    // 12. Delete the second task
    const deleteButton = page.locator('.space-y-3').getByRole('button', { name: 'Delete' }).nth(1);
    await deleteButton.click();

    // 13. Verify second task is removed
    await expect(page.getByText('Test Task 2')).not.toBeVisible();

    // 14. Verify first task still exists and is completed
    await expect(page.getByText('Test Task 1')).toBeVisible();

    // 15. Logout
    await page.getByRole('button', { name: 'Logout' }).click();

    // 16. Verify redirect to login page
    await expect(page).toHaveURL('http://localhost:3000/auth/login');

    // 17. Login again with same credentials
    await page.locator('input[type="email"]').fill(userEmail);
    await page.locator('input[type="password"]').fill(userPassword);
    await page.getByRole('button', { name: 'Login' }).click();

    // 18. Verify successful login and existing task is still there
    await expect(page).toHaveURL('http://localhost:3000/dashboard');
    await expect(page.getByText('Test Task 1')).toBeVisible();
  });

  test('should enforce user isolation - different users have separate task lists', async ({ page, context }) => {
    // Create and login as first user
    await page.goto('http://localhost:3000');

    // Signup first user
    await page.getByText('Create one here').click();
    await page.locator('input[type="email"]').fill(`user1_${Date.now()}@example.com`);
    await page.locator('input[type="password"]').fill(userPassword);
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // Create a task for first user
    await expect(page).toHaveURL('http://localhost:3000/dashboard');
    await page.locator('input[placeholder="What needs to be done?"]').fill('User 1 Task');
    await page.locator('textarea[placeholder="Add any additional details..."]').fill('Task for user 1');
    await page.getByRole('button', { name: 'Create Task' }).click();
    await expect(page.getByText('User 1 Task')).toBeVisible();

    // Logout first user
    await page.getByRole('button', { name: 'Logout' }).click();

    // Create and login as second user in a new context to simulate different session
    const newUserContext = await context.browser().newContext();
    const newUserPage = await newUserContext.newPage();

    await newUserPage.goto('http://localhost:3000');

    // Signup second user
    await newUserPage.getByText('Create one here').click();
    await newUserPage.locator('input[type="email"]').fill(`user2_${Date.now()}@example.com`);
    await newUserPage.locator('input[type="password"]').fill(userPassword);
    await newUserPage.getByRole('button', { name: 'Sign Up' }).click();

    // Verify second user has empty task list
    await expect(newUserPage).toHaveURL('http://localhost:3000/dashboard');
    await expect(newUserPage.getByText('No tasks yet')).toBeVisible();

    // Create a task for second user
    await newUserPage.locator('input[placeholder="What needs to be done?"]').fill('User 2 Task');
    await newUserPage.locator('textarea[placeholder="Add any additional details..."]').fill('Task for user 2');
    await newUserPage.getByRole('button', { name: 'Create Task' }).click();
    await expect(newUserPage.getByText('User 2 Task')).toBeVisible();

    // Verify second user cannot see first user's task
    await expect(newUserPage.getByText('User 1 Task')).not.toBeVisible();

    await newUserPage.close();
  });

  test('should handle authentication properly - protected routes', async ({ page }) => {
    // Try to access dashboard without login
    await page.goto('http://localhost:3000/dashboard');

    // Should redirect to login
    await expect(page).toHaveURL('http://localhost:3000/auth/login');
    await expect(page.getByText('Login')).toBeVisible();

    // Try to access dashboard with direct URL after login
    // First, register a user
    await page.getByText('Create one here').click();
    await page.locator('input[type="email"]').fill(`auth_test_${Date.now()}@example.com`);
    await page.locator('input[type="password"]').fill(userPassword);
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // Should be redirected to dashboard after signup
    await expect(page).toHaveURL('http://localhost:3000/dashboard');
    await expect(page.getByText('My Tasks')).toBeVisible();
  });

  test('should validate form inputs properly', async ({ page }) => {
    // Register a user first
    await page.goto('http://localhost:3000');
    await page.getByText('Create one here').click();
    await page.locator('input[type="email"]').fill(`validation_test_${Date.now()}@example.com`);
    await page.locator('input[type="password"]').fill(userPassword);
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // Try to create a task with empty title
    await page.locator('input[placeholder="What needs to be done?"]').fill('');
    await page.locator('textarea[placeholder="Add any additional details..."]').fill('Test description');
    await page.getByRole('button', { name: 'Create Task' }).click();

    // Should show validation error
    await expect(page.getByText('Task title is required')).toBeVisible();

    // Try to create a task with valid title
    await page.locator('input[placeholder="What needs to be done?"]').fill('Valid Task');
    await page.locator('textarea[placeholder="Add any additional details..."]').fill('Test description');
    await page.getByRole('button', { name: 'Create Task' }).click();

    // Should succeed
    await expect(page.getByText('Valid Task')).toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Register a user first
    await page.goto('http://localhost:3000');
    await page.getByText('Create one here').click();
    await page.locator('input[type="email"]').fill(`error_test_${Date.now()}@example.com`);
    await page.locator('input[type="password"]').fill(userPassword);
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // Verify we're on the dashboard
    await expect(page).toHaveURL('http://localhost:3000/dashboard');

    // Test error handling by trying to submit a very long title (should be rejected by validation)
    const longTitle = 'A'.repeat(256); // More than 255 characters
    await page.locator('input[placeholder="What needs to be done?"]').fill(longTitle);
    await page.locator('textarea[placeholder="Add any additional details..."]').fill('Test description');
    await page.getByRole('button', { name: 'Create Task' }).click();

    // Should show validation error for title length
    await expect(page.getByText('Title must be 255 characters or less')).toBeVisible();
  });
});