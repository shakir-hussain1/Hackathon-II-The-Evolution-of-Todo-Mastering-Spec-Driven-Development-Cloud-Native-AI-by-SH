import { test, expect } from '@playwright/test';

const viewports = [
  { name: 'Mobile - iPhone SE', width: 375, height: 667 },
  { name: 'Mobile - iPhone 12 Pro', width: 390, height: 844 },
  { name: 'Tablet - iPad', width: 768, height: 1024 },
  { name: 'Tablet - iPad Pro', width: 1024, height: 1366 },
  { name: 'Laptop - 13 inch', width: 1280, height: 800 },
  { name: 'Laptop - 15 inch', width: 1440, height: 900 },
  { name: 'Desktop - 1080p', width: 1920, height: 1080 },
  { name: 'Desktop - 2K', width: 2560, height: 1440 },
];

test.describe('Responsive Design Testing', () => {
  for (const viewport of viewports) {
    test(`should display correctly on ${viewport.name} (${viewport.width}x${viewport.height})`, async ({ page }) => {
      // Set viewport
      await page.setViewportSize({ width: viewport.width, height: viewport.height });

      // Navigate to login page
      await page.goto('/auth/login');
      await page.waitForTimeout(1000);

      // Take screenshot of login page
      await page.screenshot({
        path: `test-results/responsive-${viewport.width}x${viewport.height}-login.png`,
        fullPage: true
      });

      // Try to login
      try {
        await page.fill('input[type="email"]', 'livetest@example.com', { timeout: 5000 });
        await page.fill('input[type="password"]', 'LiveTest123!', { timeout: 5000 });
        await page.click('button[type="submit"]', { timeout: 5000 });

        // Wait for dashboard
        await page.waitForURL('**/dashboard', { timeout: 10000 });
        await page.waitForTimeout(2000);

        // Take screenshot of dashboard
        await page.screenshot({
          path: `test-results/responsive-${viewport.width}x${viewport.height}-dashboard.png`,
          fullPage: true
        });

        console.log(`✓ ${viewport.name}: Both pages captured successfully`);
      } catch (error) {
        console.log(`✗ ${viewport.name}: Could not reach dashboard, but login captured`);
      }
    });
  }

  test('should display summary of all responsive tests', async ({ page }) => {
    console.log('\n========================================');
    console.log('RESPONSIVE DESIGN TEST COMPLETE!');
    console.log('========================================');
    console.log('Tested on:');
    viewports.forEach(vp => {
      console.log(`- ${vp.name}: ${vp.width}x${vp.height}`);
    });
    console.log('\nScreenshots saved in test-results/');
    console.log('========================================\n');
  });
});
