import { test, expect } from '@playwright/test';

test.describe('Live UI Testing - Full Flow', () => {
  test('should show the complete user interface flow', async ({ page }) => {
    // Set viewport to standard desktop size
    await page.setViewportSize({ width: 1920, height: 1080 });

    // Step 1: Visit login page
    await page.goto('/auth/login');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'test-results/01-login-page.png', fullPage: true });
    console.log('✓ Screenshot 1: Login page captured');

    // Step 2: Try to login with test user
    await page.fill('input[type="email"]', 'livetest@example.com');
    await page.fill('input[type="password"]', 'LiveTest123!');
    await page.screenshot({ path: 'test-results/02-login-filled.png', fullPage: true });
    console.log('✓ Screenshot 2: Login form filled');

    // Click login
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);

    // Step 3: Dashboard should load
    await page.waitForURL('**/dashboard', { timeout: 10000 });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/03-dashboard-initial.png', fullPage: true });
    console.log('✓ Screenshot 3: Dashboard loaded');

    // Step 4: Check task form
    await page.screenshot({ path: 'test-results/04-task-form.png', fullPage: false });
    console.log('✓ Screenshot 4: Task form visible');

    // Step 5: Create a task
    await page.fill('input[placeholder="What needs to be done?"]', 'Complete documentation');
    await page.fill('textarea[placeholder="Add more details about your task..."]', 'Write comprehensive documentation for the project including setup, usage, and API reference');
    await page.waitForTimeout(500);
    await page.screenshot({ path: 'test-results/05-creating-task.png', fullPage: true });
    console.log('✓ Screenshot 5: Creating task');

    await page.click('button:has-text("Create Task")');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'test-results/06-task-created.png', fullPage: true });
    console.log('✓ Screenshot 6: Task created');

    // Step 6: Scroll to see the full dashboard
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(500);
    await page.screenshot({ path: 'test-results/07-final-dashboard.png', fullPage: true });
    console.log('✓ Screenshot 7: Final dashboard view');

    console.log('\n========================================');
    console.log('LIVE UI TEST COMPLETE!');
    console.log('========================================');
    console.log('Screenshots saved in test-results folder:');
    console.log('1. Login page');
    console.log('2. Login form filled');
    console.log('3. Dashboard initial view');
    console.log('4. Task creation form');
    console.log('5. Creating a task');
    console.log('6. Task created successfully');
    console.log('7. Final dashboard with task');
    console.log('========================================\n');
  });
});
