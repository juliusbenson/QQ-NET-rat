# Download Junghun Cho's Public Box folder for QQ

from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


sharedUrl: str = (
    # "https://wcm.app.box.com/s/v1thrs0ezuuhb13cdho1xaoiu3bd9h5j" # Entire folder
    "https://wcm.app.box.com/s/v1thrs0ezuuhb13cdho1xaoiu3bd9h5j/folder/142986360350" # Just the folder containing QQ_NET_trained_model.pt
    # "https://wcm.app.box.com/s/v1thrs0ezuuhb13cdho1xaoiu3bd9h5j/folder/142986548090" # codes
)

outputDir: Path = Path(".")
outputDir.mkdir(exist_ok=True)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)

    page = browser.new_page(
        accept_downloads=True,
    )

    # Print requests that look related to downloading or ZIP generation.
    def logRequest(request) -> None:
        url = request.url.lower()

        if any(
            term in url
            for term in (
                "download",
                "zip",
                "archive",
            )
        ):
            print(f"\n>>> REQUEST {request.method}:")
            print(request.url)

    page.on("request", logRequest)

    # Also print potentially relevant responses.
    def logResponse(response) -> None:
        url = response.url.lower()

        if any(
            term in url
            for term in (
                "download",
                "zip",
                "archive",
            )
        ):
            print(f"\n<<< RESPONSE {response.status}:")
            print(response.url)

    page.on("response", logResponse)

    print(f"Loading {sharedUrl}")

    page.goto(
        sharedUrl,
        wait_until="domcontentloaded",
        timeout=120_000,
    )

    # Let the Box application finish initializing.
    page.wait_for_timeout(5_000)

    print(f"Title: {page.title()}")

    downloadButton = page.get_by_role(
        "button",
        name="Download",
    )

    print(f"Download buttons found: {downloadButton.count()}")

    if downloadButton.count() == 0:
        raise RuntimeError("Could not find Box Download button")

    try:
        with page.expect_download(timeout=180_000) as downloadInfo:
            print("Clicking Download...")
            downloadButton.click()

        download = downloadInfo.value

        print("\n=== DOWNLOAD ===")
        print(f"Suggested filename: {download.suggested_filename}")
        print(f"URL: {download.url}")

        outputPath = outputDir / download.suggested_filename
        download.save_as(outputPath)

        print(f"Saved to: {outputPath}")
        print(f"Size: {outputPath.stat().st_size:,} bytes")

    except PlaywrightTimeoutError:
        print("\nNo direct browser download was detected.")

        print("\n=== PAGE TEXT AFTER CLICK ===")
        print(page.locator("body").inner_text()[:10_000])

        page.screenshot(
            path=outputDir / "box-after-download-click.png",
            full_page=True,
        )

        print('Please wait, Box is preparing the .zip for download. Watch the ./downloads folder...')

    browser.close()