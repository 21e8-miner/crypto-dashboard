#!/usr/bin/env python3
"""Capture Gödel Machine visualization as images"""

import asyncio
import os
from pathlib import Path

async def capture_visualization():
    from playwright.async_api import async_playwright

    html_path = Path(__file__).parent / "godel_standalone.html"
    output_dir = Path(__file__).parent / "captures"
    output_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1400, 'height': 1000})

        # Load the HTML file
        await page.goto(f"file://{html_path.absolute()}")

        # Wait for initial render
        await asyncio.sleep(2)

        # Capture multiple frames
        print("Capturing Gödel Machine visualization...")
        for i in range(5):
            screenshot_path = output_dir / f"godel_frame_{i+1}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"  Frame {i+1}/5 captured: {screenshot_path}")
            await asyncio.sleep(1.5)  # Wait for state changes

        await browser.close()

    print(f"\nCaptures saved to: {output_dir}")
    return output_dir

if __name__ == "__main__":
    asyncio.run(capture_visualization())
