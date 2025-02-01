import asyncio
from playwright.async_api import async_playwright

class PlaywrightHelper:
    async def fetch_travel_data(self, start: str, start_id: str, destination: str, destination_id: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            await page.goto("https://9292.nl")
            await page.click('button[data-testid="uc-accept-all-button"]')
            await page.fill('input[name="from"]', start)
            await page.click(f'div[id="{start_id}"]')
            await page.fill('input[name="to"]', destination)
            await page.click(f'div[id="{destination_id}"]')

            await page.click('button[data-track-event-element="journey_options"]')
            await page.click('button[id="limitWalking"]')
            await page.click('button[data-track-event-element="apply_options"]')
            await page.click('button[type="submit"]')
            await page.wait_for_selector('a[data-track-event-element="journey_list_option"]')

            travel_data = await page.evaluate('''() => {
                const journeys = [];
                document.querySelectorAll('a[data-track-event-element="journey_list_option"]').forEach(card => {
                    const departureTimeElement = card.querySelector('time[aria-label^="Geplande vertrektijd"]');
                    const arrivalTimeElement = card.querySelector('time[aria-label^="Geplande aankomsttijd"]');
                    const durationElement = card.querySelector('.journeyDuration');
                    const priceElement = card.querySelector('.journeyPrice');
                    const modalitiesElements = card.querySelectorAll('.journeyModalities svg');

                    const departureTime = departureTimeElement ? departureTimeElement.innerText : 'N/A';
                    const arrivalTime = arrivalTimeElement ? arrivalTimeElement.innerText : 'N/A';
                    const duration = durationElement ? durationElement.innerText : 'N/A';
                    const price = priceElement ? priceElement.innerText : 'N/A';
                    const modalities = Array.from(modalitiesElements).map(svg => svg.getAttribute('aria-label') || 'N/A');

                    journeys.push({
                        departureTime,
                        arrivalTime,
                        duration,
                        price,
                        modalities
                    });
                });
                return journeys;
            }''')

            await browser.close()
            return travel_data
