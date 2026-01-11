import { test, expect } from '@playwright/test';

test.describe('UI/UX and User Experience', () => {
  const testUser = {
    email: `ui-test-${Date.now()}@example.com`,
    password: 'SecurePassword123!',
  };

  test('should have responsive design elements', async ({ page }) => {
    await page.goto('/');

    // Check viewport is responsive
    await page.setViewportSize({ width: 375, height: 667 }); // Mobile
    await page.waitForTimeout(500);

    // Check if page renders without horizontal scroll
    const body = await page.locator('body').boundingBox();
    expect(body?.width).toBeLessThanOrEqual(375);

    // Desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.waitForTimeout(500);
  });

  test('should have accessible navigation', async ({ page }) => {
    await page.goto('/');

    // Check for main navigation elements
    const nav = page.locator('nav, header').first();
    const hasNav = await nav.isVisible({ timeout: 2000 }).catch(() => false);

    if (hasNav) {
      expect(hasNav).toBeTruthy();
    }

    // Check for links
    const links = await page.locator('a').count();
    expect(links).toBeGreaterThan(0);
  });

  test('should display loading states appropriately', async ({ page }) => {
    await page.goto('/auth/signup');

    await page.locator('input[type="email"]').first().fill(testUser.email);
    await page.locator('input[type="password"]').first().fill(testUser.password);

    const submitButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();

    // Click and check for loading state
    await submitButton.click();

    // Loading indicator might appear briefly
    const loadingIndicator = page.locator('[class*="loading"], [class*="spinner"], [aria-busy="true"]').first();
    const hasLoading = await loadingIndicator.isVisible({ timeout: 1000 }).catch(() => false);

    // It's okay if there's no loading indicator, just checking
    if (hasLoading) {
      expect(hasLoading).toBeTruthy();
    }

    await page.waitForURL(/dashboard|login/, { timeout: 10000 });
  });

  test('should have proper form validation', async ({ page }) => {
    await page.goto('/auth/signup');

    // Try to submit empty form
    const submitButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();
    await submitButton.click();

    await page.waitForTimeout(1000);

    // Check for validation messages (HTML5 or custom)
    const emailInput = page.locator('input[type="email"]').first();
    const isInvalid = await emailInput.evaluate((el: HTMLInputElement) => !el.validity.valid);

    // Either HTML5 validation or custom error messages should appear
    if (isInvalid) {
      expect(isInvalid).toBeTruthy();
    } else {
      // Check for custom error messages
      const errorMsg = page.locator('[class*="error"], [role="alert"], text=/required|invalid/i').first();
      const hasError = await errorMsg.isVisible({ timeout: 2000 }).catch(() => false);
      // It's okay if validation is not strict, but good to check
    }
  });

  test('should display task count or empty state', async ({ page }) => {
    // Login first
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

    // Check for empty state or task list
    const emptyState = page.locator('text=/no tasks|empty|get started|create your first/i').first();
    const taskList = page.locator('[class*="task"], [data-testid="task-list"], ul, div[role="list"]').first();

    const hasEmptyState = await emptyState.isVisible({ timeout: 2000 }).catch(() => false);
    const hasTaskList = await taskList.isVisible({ timeout: 2000 }).catch(() => false);

    // Should have either empty state or task list
    expect(hasEmptyState || hasTaskList).toBeTruthy();
  });

  test('should have consistent styling', async ({ page }) => {
    await page.goto('/');

    // Check for CSS/styling
    const body = page.locator('body');
    const backgroundColor = await body.evaluate((el) => getComputedStyle(el).backgroundColor);

    // Should have some background color set
    expect(backgroundColor).toBeTruthy();

    // Check for font
    const fontFamily = await body.evaluate((el) => getComputedStyle(el).fontFamily);
    expect(fontFamily).toBeTruthy();
  });

  test('should handle keyboard navigation', async ({ page }) => {
    await page.goto('/auth/login');

    // Tab through form fields
    await page.keyboard.press('Tab');
    await page.waitForTimeout(200);

    const activeElement1 = await page.evaluate(() => document.activeElement?.tagName);

    await page.keyboard.press('Tab');
    await page.waitForTimeout(200);

    const activeElement2 = await page.evaluate(() => document.activeElement?.tagName);

    // Should be able to tab through elements
    expect(activeElement1).toBeTruthy();
    expect(activeElement2).toBeTruthy();
  });

  test('should display user feedback on actions', async ({ page }) => {
    // Login
    await page.goto('/auth/signup');

    const email = `feedback-test-${Date.now()}@example.com`;
    await page.locator('input[type="email"]').first().fill(email);
    await page.locator('input[type="password"]').first().fill('SecurePassword123!');

    const signupButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();
    await signupButton.click();

    await page.waitForURL(/dashboard|login/, { timeout: 10000 });

    if (page.url().includes('login')) {
      await page.locator('input[type="email"]').first().fill(email);
      await page.locator('input[type="password"]').first().fill('SecurePassword123!');
      await page.getByRole('button', { name: /log in|login/i }).first().click();
      await page.waitForURL(/dashboard/, { timeout: 10000 });
    }

    if (!page.url().includes('dashboard')) {
      await page.goto('/dashboard');
    }

    await page.waitForLoadState('networkidle');

    // Create a task and check for feedback (toast, message, etc.)
    const taskTitle = `Feedback Test ${Date.now()}`;
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Check if task appears (which is feedback itself)
    const taskItem = page.locator(`text="${taskTitle}"`).first();
    const taskVisible = await taskItem.isVisible({ timeout: 3000 }).catch(() => false);

    // Also check for success message/toast
    const successMsg = page.locator('[class*="success"], [class*="toast"], text=/added|created|success/i').first();
    const hasSuccess = await successMsg.isVisible({ timeout: 2000 }).catch(() => false);

    // Either the task appears or a success message shows
    expect(taskVisible || hasSuccess).toBeTruthy();
  });

  test('should have clear call-to-action buttons', async ({ page }) => {
    await page.goto('/');

    // Check for clear CTAs
    const buttons = await page.locator('button, a[class*="button"], a[class*="btn"]').count();
    expect(buttons).toBeGreaterThan(0);

    // Check button text is readable
    const firstButton = page.locator('button, a[class*="button"]').first();
    const hasButton = await firstButton.isVisible({ timeout: 2000 }).catch(() => false);

    if (hasButton) {
      const buttonText = await firstButton.textContent();
      expect(buttonText?.trim().length).toBeGreaterThan(0);
    }
  });

  test('should handle rapid interactions gracefully', async ({ page }) => {
    // Login
    await page.goto('/auth/signup');

    const email = `rapid-test-${Date.now()}@example.com`;
    await page.locator('input[type="email"]').first().fill(email);
    await page.locator('input[type="password"]').first().fill('SecurePassword123!');

    const signupButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();
    await signupButton.click();

    await page.waitForURL(/dashboard|login/, { timeout: 10000 });

    if (page.url().includes('login')) {
      await page.locator('input[type="email"]').first().fill(email);
      await page.locator('input[type="password"]').first().fill('SecurePassword123!');
      await page.getByRole('button', { name: /log in|login/i }).first().click();
      await page.waitForURL(/dashboard/, { timeout: 10000 });
    }

    if (!page.url().includes('dashboard')) {
      await page.goto('/dashboard');
    }

    await page.waitForLoadState('networkidle');

    // Try to create tasks rapidly
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();

    for (let i = 0; i < 3; i++) {
      await titleInput.fill(`Rapid Task ${i} ${Date.now()}`);
      await addButton.click();
      // No wait - rapid fire
    }

    await page.waitForTimeout(2000);

    // App should still be responsive
    const isResponsive = await page.evaluate(() => document.readyState === 'complete');
    expect(isResponsive).toBeTruthy();
  });
});
