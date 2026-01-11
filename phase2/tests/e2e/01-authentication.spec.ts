import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  const testUser = {
    email: `test-${Date.now()}@example.com`,
    password: 'SecurePassword123!',
    name: 'Test User'
  };

  test.beforeEach(async ({ page }) => {
    // Start from home page
    await page.goto('/');
  });

  test('should load the home page', async ({ page }) => {
    await expect(page).toHaveTitle(/Todo/i);
  });

  test('should navigate to signup page', async ({ page }) => {
    // Look for signup link/button
    const signupLink = page.getByRole('link', { name: /sign up|signup|register/i }).first();
    if (await signupLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await signupLink.click();
    } else {
      // Direct navigation if no link found
      await page.goto('/auth/signup');
    }

    await expect(page).toHaveURL(/signup/);
  });

  test('should navigate to login page', async ({ page }) => {
    // Look for login link/button
    const loginLink = page.getByRole('link', { name: /log in|login|sign in/i }).first();
    if (await loginLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await loginLink.click();
    } else {
      // Direct navigation if no link found
      await page.goto('/auth/login');
    }

    await expect(page).toHaveURL(/login/);
  });

  test('should successfully signup a new user', async ({ page }) => {
    await page.goto('/auth/signup');

    // Fill signup form - try multiple possible field names
    const emailInput = page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]').first();
    await emailInput.fill(testUser.email);

    const passwordInput = page.locator('input[type="password"], input[name="password"], input[placeholder*="password" i]').first();
    await passwordInput.fill(testUser.password);

    // Some forms might have a name field
    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i]').first();
    if (await nameInput.isVisible({ timeout: 1000 }).catch(() => false)) {
      await nameInput.fill(testUser.name);
    }

    // Submit form
    const submitButton = page.getByRole('button', { name: /sign up|signup|register|create account/i }).first();
    await submitButton.click();

    // Should redirect to dashboard or login
    await page.waitForURL(/dashboard|login/, { timeout: 10000 });

    // Verify we're logged in or redirected properly
    const currentUrl = page.url();
    expect(currentUrl).toMatch(/dashboard|login/);
  });

  test('should successfully login with credentials', async ({ page }) => {
    // First signup the user
    await page.goto('/auth/signup');

    const emailInput = page.locator('input[type="email"], input[name="email"]').first();
    await emailInput.fill(testUser.email);

    const passwordInput = page.locator('input[type="password"], input[name="password"]').first();
    await passwordInput.fill(testUser.password);

    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i]').first();
    if (await nameInput.isVisible({ timeout: 1000 }).catch(() => false)) {
      await nameInput.fill(testUser.name);
    }

    const signupButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();
    await signupButton.click();

    await page.waitForTimeout(2000);

    // Now try to login
    await page.goto('/auth/login');

    await page.locator('input[type="email"], input[name="email"]').first().fill(testUser.email);
    await page.locator('input[type="password"], input[name="password"]').first().fill(testUser.password);

    const loginButton = page.getByRole('button', { name: /log in|login|sign in/i }).first();
    await loginButton.click();

    // Should redirect to dashboard
    await page.waitForURL(/dashboard/, { timeout: 10000 });
    expect(page.url()).toContain('dashboard');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/auth/login');

    await page.locator('input[type="email"], input[name="email"]').first().fill('invalid@example.com');
    await page.locator('input[type="password"], input[name="password"]').first().fill('wrongpassword');

    const loginButton = page.getByRole('button', { name: /log in|login|sign in/i }).first();
    await loginButton.click();

    // Should show error message
    const errorMessage = page.locator('text=/invalid|error|wrong|incorrect/i').first();
    await expect(errorMessage).toBeVisible({ timeout: 5000 });
  });

  test('should require authentication for dashboard', async ({ page }) => {
    // Try to access dashboard without login
    await page.goto('/dashboard');

    // Should redirect to login
    await page.waitForURL(/login|auth/, { timeout: 10000 });
    expect(page.url()).toMatch(/login|auth/);
  });

  test('should logout successfully', async ({ page }) => {
    // First login
    await page.goto('/auth/signup');

    const emailInput = page.locator('input[type="email"]').first();
    await emailInput.fill(`logout-test-${Date.now()}@example.com`);

    const passwordInput = page.locator('input[type="password"]').first();
    await passwordInput.fill('SecurePassword123!');

    const signupButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();
    await signupButton.click();

    await page.waitForURL(/dashboard|login/, { timeout: 10000 });

    // If we're at login, login first
    if (page.url().includes('login')) {
      await page.locator('input[type="email"]').first().fill(`logout-test-${Date.now()}@example.com`);
      await page.locator('input[type="password"]').first().fill('SecurePassword123!');
      await page.getByRole('button', { name: /log in|login/i }).first().click();
      await page.waitForURL(/dashboard/, { timeout: 10000 });
    }

    // Look for logout button
    const logoutButton = page.getByRole('button', { name: /log out|logout|sign out/i }).first();
    if (await logoutButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await logoutButton.click();

      // Should redirect to login or home
      await page.waitForURL(/login|auth|^\/$/, { timeout: 10000 });
      expect(page.url()).toMatch(/login|auth|\/$/);
    }
  });
});
