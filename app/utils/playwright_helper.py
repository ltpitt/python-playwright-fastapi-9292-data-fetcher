import asyncio
from playwright.async_api import async_playwright

class PlaywrightHelper:
    async def fetch_travel_data(self, start: str, start_id: str, destination: str, destination_id: str):
        """
        Fetch travel data from 9292.nl using improved selectors and error handling.
        
        Note: start_id and destination_id parameters are kept for API compatibility
        but are not used since we use combobox + autocomplete approach.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                print(f"Navigating to 9292.nl...")
                await page.goto("https://9292.nl", wait_until='networkidle')
                
                # Handle cookie consent if it appears
                try:
                    cookie_button = page.get_by_test_id('uc-accept-all-button')
                    await cookie_button.click(timeout=5000)
                    print("✓ Accepted cookies")
                except Exception:
                    print("✓ No cookie dialog (already accepted or not shown)")
                
                # Fill in departure location using combobox
                print(f"Setting departure: {start}")
                from_field = page.get_by_role('combobox', name='Van')
                await from_field.fill('')  # Clear first
                await from_field.press_sequentially(start, delay=100)
                await page.wait_for_timeout(1000)  # Wait for autocomplete
                
                # Select first option from autocomplete
                try:
                    first_option = page.get_by_role('option').first
                    await first_option.click(timeout=5000)
                    print(f"✓ Selected departure location")
                except Exception as e:
                    print(f"✗ Could not select departure: {e}")
                    await page.screenshot(path='error_departure.png')
                    raise
                
                # Fill in destination location
                print(f"Setting destination: {destination}")
                to_field = page.get_by_role('combobox', name='Naar')
                await to_field.fill('')  # Clear first
                await to_field.press_sequentially(destination, delay=100)
                await page.wait_for_timeout(1000)  # Wait for autocomplete
                
                # Select first option from autocomplete
                try:
                    first_option = page.get_by_role('option').first
                    await first_option.click(timeout=5000)
                    print(f"✓ Selected destination location")
                except Exception as e:
                    print(f"✗ Could not select destination: {e}")
                    await page.screenshot(path='error_destination.png')
                    raise
                
                # Click the search button
                print("Submitting search...")
                search_button = page.get_by_role('button', name='Plan je reis')
                await search_button.click()
                
                # Wait for results page to load
                await page.wait_for_load_state('networkidle')
                print("✓ Results page loaded")
                
                # Extract journey data from the results
                print("Extracting journey data...")
                travel_data = await page.evaluate('''() => {
                    const journeys = [];
                    
                    // Find all journey links - these contain the journey options
                    const journeyLinks = document.querySelectorAll('a[href*="/reisplanner/"]');
                    
                    journeyLinks.forEach(link => {
                        try {
                            // Extract time elements
                            const times = link.querySelectorAll('time');
                            const departureTime = times[0]?.textContent?.trim() || 'N/A';
                            const arrivalTime = times[times.length - 1]?.textContent?.trim() || 'N/A';
                            
                            // Extract duration (looks for text like "25m", "1u 30m")
                            const durationElement = Array.from(link.querySelectorAll('*')).find(el => 
                                /^\\d+(m|u|h)/.test(el.textContent.trim()) && el.textContent.length < 10
                            );
                            const duration = durationElement?.textContent?.trim() || 'N/A';
                            
                            // Extract price (looks for € symbol)
                            const priceElement = Array.from(link.querySelectorAll('*')).find(el => 
                                el.textContent.includes('€') && el.textContent.length < 20
                            );
                            const price = priceElement?.textContent?.trim() || 'N/A';
                            
                            // Extract transport modalities from images
                            const modalityImages = link.querySelectorAll('img');
                            const modalities = Array.from(modalityImages)
                                .map(img => img.alt || img.getAttribute('aria-label'))
                                .filter(alt => alt && !alt.includes('logo') && !alt.includes('icon'));
                            
                            // Only add if we have at least departure and arrival times
                            if (departureTime !== 'N/A' && arrivalTime !== 'N/A') {
                                journeys.push({
                                    departureTime,
                                    arrivalTime,
                                    duration,
                                    price,
                                    modalities: modalities.length > 0 ? modalities : ['Unknown']
                                });
                            }
                        } catch (error) {
                            console.error('Error parsing journey:', error);
                        }
                    });
                    
                    return journeys;
                }''')
                
                print(f"✓ Found {len(travel_data)} journeys")
                
                if len(travel_data) == 0:
                    print("⚠ No journeys found, taking debug screenshot...")
                    await page.screenshot(path='debug_no_results.png')
                
                return travel_data
                
            except Exception as e:
                print(f"✗ Error during scraping: {e}")
                await page.screenshot(path='error_final.png')
                raise
            finally:
                await browser.close()
