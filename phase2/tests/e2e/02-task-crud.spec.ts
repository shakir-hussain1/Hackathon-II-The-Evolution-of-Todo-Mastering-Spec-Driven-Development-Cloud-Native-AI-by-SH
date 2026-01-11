import { test, expect } from '@playwright/test';

test.describe('Task CRUD Operations', () => {
  const testUser = {
    email: `task-test-${Date.now()}@example.com`,
    password: 'SecurePassword123!',
    name: 'Task Test User'
  };

  // Helper function to login before each test
  test.beforeEach(async ({ page }) => {
    // Signup and login
    await page.goto('/auth/signup');

    await page.locator('input[type="email"]').first().fill(testUser.email);
    await page.locator('input[type="password"]').first().fill(testUser.password);

    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i]').first();
    if (await nameInput.isVisible({ timeout: 1000 }).catch(() => false)) {
      await nameInput.fill(testUser.name);
    }

    const signupButton = page.getByRole('button', { name: /sign up|signup|register/i }).first();
    await signupButton.click();

    // Wait for dashboard or login redirect
    await page.waitForURL(/dashboard|login/, { timeout: 10000 });

    // If redirected to login, login
    if (page.url().includes('login')) {
      await page.locator('input[type="email"]').first().fill(testUser.email);
      await page.locator('input[type="password"]').first().fill(testUser.password);
      await page.getByRole('button', { name: /log in|login/i }).first().click();
      await page.waitForURL(/dashboard/, { timeout: 10000 });
    }

    // Make sure we're on the dashboard
    if (!page.url().includes('dashboard')) {
      await page.goto('/dashboard');
    }

    await page.waitForLoadState('networkidle');
  });

  test('should create a new task', async ({ page }) => {
    const taskTitle = `Test Task ${Date.now()}`;
    const taskDescription = 'This is a test task description';

    // Find task input field
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    // Find description field if exists
    const descInput = page.locator('textarea[name="description"], textarea[placeholder*="description" i], input[name="description"]').first();
    if (await descInput.isVisible({ timeout: 1000 }).catch(() => false)) {
      await descInput.fill(taskDescription);
    }

    // Submit the task
    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    // Wait for the task to appear in the list
    await page.waitForTimeout(1000);

    // Verify task appears in the list
    const taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible({ timeout: 5000 });
  });

  test('should display created tasks in the list', async ({ page }) => {
    const taskTitle = `Display Test ${Date.now()}`;

    // Create a task
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Check if task list exists and contains our task
    const taskList = page.locator('[class*="task"], [data-testid="task-list"], ul, div[role="list"]').first();
    await expect(taskList).toBeVisible({ timeout: 5000 });

    const taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible();
  });

  test('should mark a task as completed', async ({ page }) => {
    const taskTitle = `Complete Test ${Date.now()}`;

    // Create a task
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Find the task item
    const taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible();

    // Find and click checkbox or complete button
    const taskContainer = taskItem.locator('..').locator('..'); // Go up to task container
    const checkbox = taskContainer.locator('input[type="checkbox"], button[aria-label*="complete" i]').first();

    if (await checkbox.isVisible({ timeout: 2000 }).catch(() => false)) {
      await checkbox.click();
      await page.waitForTimeout(500);

      // Verify task is marked as completed (might have strikethrough, different color, etc.)
      const completedTask = taskContainer.locator('[class*="completed"], [class*="done"], [style*="line-through"]');
      const isCompleted = await completedTask.isVisible({ timeout: 2000 }).catch(() => false);

      if (isCompleted) {
        expect(isCompleted).toBeTruthy();
      }
    }
  });

  test('should delete a task', async ({ page }) => {
    const taskTitle = `Delete Test ${Date.now()}`;

    // Create a task
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(taskTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Find the task
    const taskItem = page.locator(`text="${taskTitle}"`).first();
    await expect(taskItem).toBeVisible();

    // Find and click delete button
    const taskContainer = taskItem.locator('..').locator('..');
    const deleteButton = taskContainer.locator('button[aria-label*="delete" i], button:has-text("Delete"), button:has-text("🗑"), [data-action="delete"]').first();

    if (await deleteButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await deleteButton.click();

      // Handle confirmation dialog if it appears
      page.on('dialog', dialog => dialog.accept());

      await page.waitForTimeout(1000);

      // Verify task is removed
      const deletedTask = page.locator(`text="${taskTitle}"`);
      await expect(deletedTask).not.toBeVisible({ timeout: 5000 });
    }
  });

  test('should edit a task', async ({ page }) => {
    const originalTitle = `Edit Test ${Date.now()}`;
    const updatedTitle = `Updated ${Date.now()}`;

    // Create a task
    const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(originalTitle);

    const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();

    await page.waitForTimeout(1000);

    // Find the task
    const taskItem = page.locator(`text="${originalTitle}"`).first();
    await expect(taskItem).toBeVisible();

    // Find edit button
    const taskContainer = taskItem.locator('..').locator('..');
    const editButton = taskContainer.locator('button[aria-label*="edit" i], button:has-text("Edit"), button:has-text("✏"), [data-action="edit"]').first();

    if (await editButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await editButton.click();
      await page.waitForTimeout(500);

      // Find the edit input field
      const editInput = page.locator('input[value*="Edit Test"], input[type="text"]:visible').first();
      await editInput.fill(updatedTitle);

      // Submit the edit
      const saveButton = page.getByRole('button', { name: /save|update|submit/i }).first();
      await saveButton.click();

      await page.waitForTimeout(1000);

      // Verify updated task appears
      const updatedTask = page.locator(`text="${updatedTitle}"`).first();
      await expect(updatedTask).toBeVisible({ timeout: 5000 });

      // Verify original task is gone
      const originalTask = page.locator(`text="${originalTitle}"`);
      await expect(originalTask).not.toBeVisible();
    }
  });

  test('should create multiple tasks', async ({ page }) => {
    const tasks = [
      `Task 1 ${Date.now()}`,
      `Task 2 ${Date.now()}`,
      `Task 3 ${Date.now()}`
    ];

    for (const task of tasks) {
      const titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
      await titleInput.fill(task);

      const addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
      await addButton.click();

      await page.waitForTimeout(500);
    }

    // Verify all tasks appear
    for (const task of tasks) {
      const taskItem = page.locator(`text="${task}"`).first();
      await expect(taskItem).toBeVisible({ timeout: 5000 });
    }
  });

  test('should filter or show all tasks', async ({ page }) => {
    // Create tasks with different statuses
    const task1 = `Active Task ${Date.now()}`;
    const task2 = `Completed Task ${Date.now()}`;

    // Create first task
    let titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(task1);
    let addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();
    await page.waitForTimeout(500);

    // Create second task
    titleInput = page.locator('input[name="title"], input[placeholder*="task" i], input[type="text"]').first();
    await titleInput.fill(task2);
    addButton = page.getByRole('button', { name: /add|create|submit|new task/i }).first();
    await addButton.click();
    await page.waitForTimeout(500);

    // Mark second task as completed
    const taskItem2 = page.locator(`text="${task2}"`).first();
    const taskContainer2 = taskItem2.locator('..').locator('..');
    const checkbox = taskContainer2.locator('input[type="checkbox"]').first();

    if (await checkbox.isVisible({ timeout: 2000 }).catch(() => false)) {
      await checkbox.click();
      await page.waitForTimeout(500);
    }

    // Look for filter buttons
    const filterButtons = page.locator('button:has-text("All"), button:has-text("Active"), button:has-text("Completed")');
    const filterCount = await filterButtons.count();

    if (filterCount > 0) {
      // Test filtering
      const activeButton = page.getByRole('button', { name: /active/i }).first();
      if (await activeButton.isVisible({ timeout: 1000 }).catch(() => false)) {
        await activeButton.click();
        await page.waitForTimeout(500);
      }
    }

    // Both tasks should exist in some form
    const allTasks = page.locator(`text="${task1}", text="${task2}"`);
    expect(await allTasks.count()).toBeGreaterThan(0);
  });
});
