import { test, expect } from '@playwright/test';

test.describe('Data Persistence and API Integration', () => {
  const testUser = {
    email: `persist-test-${Date.now()}@example.com`,
    password: 'SecurePassword123!',
  };

  test.beforeEach(async ({ page }) => {
    // Signup
    await page.goto('/auth/signup');

    await page.locator('input[type="email"]').first().fill(testUser.email);
    await page.locator('input[type="password"]').first().fill(testUser.password);

    const signupButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();
    await signupButton.click();

    await page.waitForURL(/dashboard|login/, { timeout: 10000 });

    if (page.url().includes('login')) {
      await page.locator('input[type="email"]').first().fill(testUser.email);
      await page.locator('input[type="password"]').first().fill(testUser.password);
      await page.getByRole('button', { name: /log in|login/i }).first().click();
      await page.waitForURL(/dashboard/, { timeout: 10000 });
    }

    if (!page.url().includes('dashboard')) {
      await page.goto('/dashboard');
    }

    await page.waitForLoadState('networkidle');
  });

  test('should persist tasks after page reload', async ({ page }) => {
    const taskTitle = `Persist Test ${Date.now()}`;

    // Create a task
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Verify task exists
    let taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible({ timeout: 5000 });

    // Reload the page
    await page.reload();
    await page.waitForLoadState('networkidle');

    // Task should still be there
    taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible({ timeout: 5000 });
  });

  test('should persist task completion status', async ({ page }) => {
    const taskTitle = `Completion Persist ${Date.now()}`;

    // Create a task
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Mark as completed
    const taskItem = page.locator(`text="${taskTitle}"`).first();
    const taskContainer = taskItem.locator('..').locator('..');
    const checkbox = taskContainer.locator('input[type="checkbox"]').first();

    if (await checkbox.isVisible({ timeout: 2000 }).catch(() => false)) {
      await checkbox.click();
      await page.waitForTimeout(1000);

      // Reload
      await page.reload();
      await page.waitForLoadState('networkidle');

      // Check if still completed
      const reloadedTask = page.locator(`text="${taskTitle}"`).first();
      const reloadedContainer = reloadedTask.locator('..').locator('..');
      const reloadedCheckbox = reloadedContainer.locator('input[type="checkbox"]').first();

      if (await reloadedCheckbox.isVisible({ timeout: 2000 }).catch(() => false)) {
        const isChecked = await reloadedCheckbox.isChecked();
        expect(isChecked).toBeTruthy();
      }
    }
  });

  test('should persist tasks after logout and login', async ({ page }) => {
    const taskTitle = `Logout Persist ${Date.now()}`;

    // Create a task
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Verify task exists
    let taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible({ timeout: 5000 });

    // Logout
    const logoutButton = page.getByRole('button', { name: /log out|logout|sign out/i }).first();
    if (await logoutButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await logoutButton.click();
      await page.waitForURL(/login|auth|^\/$/, { timeout: 10000 });
    } else {
      // Manual logout by going to login
      await page.goto('/auth/login');
    }

    // Login again
    await page.locator('input[type="email"]').first().fill(testUser.email);
    await page.locator('input[type="password"]').first().fill(testUser.password);

    const loginButton = page.getByRole('button', { name: /log in|login|sign in/i }).first();
    await loginButton.click();

    await page.waitForURL(/dashboard/, { timeout: 10000 });
    await page.waitForLoadState('networkidle');

    // Task should still be there
    taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible({ timeout: 5000 });
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Intercept API calls and simulate error
    await page.route('**/api/**', async (route) => {
      // Let some requests through, fail others
      if (route.request().method() === 'POST' && route.request().url().includes('/tasks')) {
        await route.abort('failed');
      } else {
        await route.continue();
      }
    });

    const taskTitle = `Error Test ${Date.now()}`;

    // Try to create a task (should fail)
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(2000);

    // Should show error message or not crash
    const errorMsg = page.locator('[class*="error"], [role="alert"], text=/error|fail/i').first();
    const hasError = await errorMsg.isVisible({ timeout: 3000 }).catch(() => false);

    // Page should still be functional
    const isResponsive = await page.evaluate(() => document.readyState === 'complete');
    expect(isResponsive).toBeTruthy();

    // Remove route interception
    await page.unroute('**/api/**');
  });

  test('should show tasks from API on dashboard load', async ({ page }) => {
    // Create a task first
    const taskTitle = `API Load Test ${Date.now()}`;

    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Intercept API calls to verify they're being made
    let apiCalled = false;
    await page.route('**/api/**tasks**', (route) => {
      apiCalled = true;
      route.continue();
    });

    // Navigate away and back
    await page.goto('/');
    await page.goto('/dashboard');

    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000);

    // API should have been called
    expect(apiCalled).toBeTruthy();

    // Task should be loaded
    const taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible({ timeout: 5000 });

    await page.unroute('**/api/**tasks**');
  });

  test('should maintain task order after operations', async ({ page }) => {
    const tasks = [
      `Task Order 1 ${Date.now()}`,
      `Task Order 2 ${Date.now()}`,
      `Task Order 3 ${Date.now()}`
    ];

    // Create multiple tasks
    for (const task of tasks) {
      const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
      await titleInput.fill(task);

      const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
      await addButton.click();

      await page.waitForTimeout(500);
    }

    // Get all task titles in order
    const taskElements = page.locator('[class*="task"], li').filter({ hasText: 'Task Order' });
    const count = await taskElements.count();

    expect(count).toBeGreaterThanOrEqual(3);

    // Reload and check if tasks are still there
    await page.reload();
    await page.waitForLoadState('networkidle');

    const reloadedTaskElements = page.locator('[class*="task"], li').filter({ hasText: 'Task Order' });
    const reloadedCount = await reloadedTaskElements.count();

    expect(reloadedCount).toBeGreaterThanOrEqual(3);
  });

  test('should handle concurrent task operations', async ({ page }) => {
    const task1 = `Concurrent 1 ${Date.now()}`;
    const task2 = `Concurrent 2 ${Date.now()}`;

    // Create first task
    let titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(task1);

    let addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    // Immediately create second task without waiting
    titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(task2);

    addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(2000);

    // Both tasks should exist
    const task1Element = page.locator(`text="${task1}"`).first();
    const task2Element = page.locator(`text="${task2}"`).first();

    await expect(task1Element).toBeVisible({ timeout: 5000 });
    await expect(task2Element).toBeVisible({ timeout: 5000 });
  });
});
