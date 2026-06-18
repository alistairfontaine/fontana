import urllib.request
import re
import os

class FontanaDataHarvester:
    def __init__(self):
        # Point directly to your clean public repository homepage layout
        self.target_url = "https://github.com/alistairfontaine/fontana"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(os.path.dirname(script_dir), "dataset.txt")

    def harvest_readme_corpus(self):
        print("==================================================")
        print(f"📡 [FONTANA SCRAPER] Connecting to public URL: {self.target_url}")
        print("==================================================")

        try:
            # Open standard network connection stream channel
            req = urllib.request.Request(self.target_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                raw_html = response.read().decode('utf-8')

            print("[PROCESS] Streaming page content... Stripping HTML formatting elements...")

            # Isolate text elements within the main description blocks to avoid script pollution
            # This captures your readme content directly from the HTML stream
            text_content = re.findall(r'<article[^>]*>(.*?)</article>', raw_html, re.DOTALL)

            if not text_content:
                # Fallback to general text parsing if article tags are compiled differently
                text_content = [raw_html]

            # Strip html tags, punctuation clutter, and script markers cleanly
            clean_text = re.sub(r'<[^>]+>', ' ', text_content[0])
            clean_text = re.sub(r'[#\*`\-\[\]\(\)\{\}\=\_\:\;\/\"]', ' ', clean_text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip().lower()

            # Safeguard text length block to prevent empty appends
            if len(clean_text) > 100:
                # Crop extreme trailing HTML noise blocks to preserve matrix purity
                clean_text = clean_text[:2000]

                with open(self.output_path, "a", encoding="utf-8") as f:
                    f.write("\n" + clean_text + " .")
                print(f"[SUCCESS] Appended harvested text corpus data to: {self.output_path}")
            else:
                print("[WARNING] Extraction layout returned insufficient text blocks.")

        except Exception as e:
            print(f"❌ [PIPELINE BLOCKED] Web harvesting failed. Details: {e}")

if __name__ == "__main__":
    harvester = FontanaDataHarvester()
    harvester.harvest_readme_corpus()
