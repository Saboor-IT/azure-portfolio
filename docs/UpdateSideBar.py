import os
from bs4 import BeautifulSoup

# Folder that contains the HTML files
folder_path = "C:\\Users\\Saboor\\Documents\\azure-portfolio"   # <- change to your folder

# HTML snippet to insert
new_li_html = '''
<li>
  <details id="DefenseDropdown">
    <summary style="color: #fff; font-size: 18px; cursor: pointer;">
      Defense-in-Depth Security Lab
    </summary>
    <ul style="padding-left: 20px; margin-top: 10px;">
      <li><a href="DefenceProject.html">Overview</a></li>
    </ul>
  </details>
</li>
'''

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".html"):
        full_path = os.path.join(folder_path, filename)

        # Read the HTML file
        with open(full_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        pen_testing = soup.find("details", id="penTestingDropdown")
        projects = soup.find("details", id="projectsDropdown")

        if pen_testing and projects:
            # Only insert if not already present (avoid duplicates)
            if not soup.find("details", id="DefenseDropdown"):
                new_li = BeautifulSoup(new_li_html, "html.parser")
                projects.insert_before(new_li)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(str(soup))
                print(f"Updated: {filename}")
            else:
                print(f"Skipped (already has DefenseDropdown): {filename}")
        else:
            print(f"Skipped (required sections missing): {filename}")