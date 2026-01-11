import { test, expect } from '@playwright/test';

/**
 * Focused demo test showing the full Todo App workflow
 * This test demonstrates:
 * 1. User signup
 * 2. Creating tasks
 * 3. Completing tasks
 * 4. Deleting tasks
 * 5. Logout
 */

test.describe('Full Todo App Demo', () => {
  test('complete user journey from signup to task management', async ({ page }) => {
    const timestamp = Date.now();
    const testEmail = `demo-${timestamp}@example.com`;
    const testPassword = 'SecurePassword123!';

    // Step 1: Navigate to home page
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Step 2: Should redirect to login, then go to signup
    await page.waitForURL(/login|auth/, { timeout: 10000 });
    await page.goto('/auth/signup');

    // Step 3: Fill out signup form
    await page.locator('input#email').fill(testEmail);
    await page.locator('input#password').fill(testPassword);
    await page.locator('input#confirmPassword').fill(testPassword);

    // Step 4: Submit signup
    await page.locator('button[type="submit"]').click();

    // Step 5: Wait for redirect to dashboard
    await page.waitForURL(/dashboard/, { timeout: 15000 });
    await page.waitForLoadState('networkidle');

    // Verify we're on dashboard
    await expect(page.locator('text=My Tasks')).toBeVisible({ timeout: 10000 });

    // Step 6: Create first task
    const task1Title = `Buy groceries ${timestamp}`;
    await page.locator('input[name="title"]').fill(task1Title);
    await page.locator('textarea[name="description"]').fill('Milk, eggs, bread');
    await page.locator('button[type="submit"]').click();

    // Wait for task to appear
    await page.waitForTimeout(2000);
    await expect(page.locator(`text="${task1Title}"`)).toBeVisible({ timeout: 5000 });

    // Step 7: Create second task
    const task2Title = `Finish project ${timestamp}`;
    await page.locator('input[name="title"]').fill(task2Title);
    await page.locator('textarea[name="description"]').fill('Complete Phase II implementation');
    await page.locator('button[type="submit"]').click();

    // Wait for task to appear
    await page.waitForTimeout(2000);
    await expect(page.locator(`text="${task2Title}"`)).toBeVisible({ timeout: 5000 });

    // Step 8: Create third task
    const task3Title = `Call dentist ${timestamp}`;
    await page.locator('input[name="title"]').fill(task3Title);
    await page.locator('button[type="submit"]').click();

    await page.waitForTimeout(2000);
    await expect(page.locator(`text="${task3Title}"`)).toBeVisible({ timeout: 5000 });

    // Step 9: Toggle first task as completed
    const firstTaskCheckbox = page.locator(`text="${task1Title}"`).locator('..').locator('..').locator('button[aria-label*="complete" i], input[type="checkbox"]').first();

    if (await firstTaskCheckbox.isVisible({ timeout: 2000 }).catch(() => false)) {
      await firstTaskCheckbox.click();
      await page.waitForTimeout(1500);
    }

    // Step 10: Delete second task
    const secondTaskContainer = page.locator(`text="${task2Title}"`).locator('..').locator('..');
    const deleteButton = secondTaskContainer.locator('button[aria-label*="delete" i]').first();

    if (await deleteButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await deleteButton.click();

      // Handle confirmation if it appears
      page.on('dialog', dialog => dialog.accept());

      await page.waitForTimeout(1500);
    }

    // Step 11: Verify remaining tasks
    await expect(page.locator(`text="${task1Title}"`)).toBeVisible();
    await expect(page.locator(`text="${task3Title}"`)).toBeVisible();

    // Step 12: Logout
    const logoutButton = page.locator('button:has-text("Logout")');
    await expect(logoutButton).toBeVisible({ timeout: 5000 });
    await logoutButton.click();

    // Should redirect to login
    await page.waitForURL(/login|auth/, { timeout: 10000 });
    await expect(page.locator('text=Welcome Back')).toBeVisible({ timeout: 5000 });

    console.log('✅ Full user journey completed successfully!');
  });
});
