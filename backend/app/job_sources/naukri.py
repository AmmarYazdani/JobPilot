from playwright.sync_api import sync_playwright

from app.job_sources.base import JobSource


class NaukriJobSource(JobSource):

    def search_jobs(self, job_title: str) -> list[dict]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(
                "https://www.naukri.com/",
                wait_until="domcontentloaded"
            )

            print("Naukri opened successfully")

            # Close cookie popup
            got_it = page.get_by_text("Got it", exact=True)

            if got_it.count() > 0:
                got_it.click()
                print("Cookie popup closed")

            # Find search box
            search_input = page.locator(
                'input[placeholder="Enter skills / designations / companies"]'
            )

            # Enter job title
            search_input.fill(job_title)

            print("Job title entered:", job_title)

            # Click Search
            search_input.press("Enter")
            print("Search initiated")

            

            # Wait for results
            page.wait_for_timeout(5000)

            jobs = []

            links = page.locator("a")

            for i in range(links.count()):
                link = links.nth(i)

                text = link.inner_text().strip()
                herf = link.get_attribute("href")

                if (
                    text and herf 
                    and herf.startswith("https://www.naukri.com/job-listings-")
                ):
                    jobs.append({
                        "title": text,
                        "url": herf
                    })

                    if len(jobs) >= 20:
                        break

            print("Jobs found:", len(jobs))
            



            input("press enter to close the browser..")

            browser.close()

        return jobs

    def apply_to_job(self, job: dict) -> dict:
        return {
            "status": "not_implemented"
        }