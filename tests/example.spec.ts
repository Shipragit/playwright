import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // ❌ Intentionally wrong
  await expect(page).toHaveTitle(/Google/);
});

test('get started link', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  await page.getByRole('link', { name: 'Get started' }).click();

  await expect(
    page.getByRole('heading', { name: 'Installation' })
  ).toBeVisible();
});