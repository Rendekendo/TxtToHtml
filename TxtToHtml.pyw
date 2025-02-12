import os
import subprocess
import requests
from urllib.parse import urlparse

def get_favicon_url(website_url):
    parsed_url = urlparse(website_url)
    favicon_url = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
    return favicon_url

def load_links_and_descriptions(filename):
    links_and_descriptions = []
    current_section = None
    
    with open(filename, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line: 
                if not line.startswith("https://"):
                    current_section = line  
                    links_and_descriptions.append((current_section, []))
                else:
                    if current_section:
                        parts = line.split(maxsplit=1)
                        if len(parts) == 2:  # Ensure valid format
                            links_and_descriptions[-1][1].append(parts)
                        else:
                            print(f"Skipping invalid line (missing description or link): {line}")
                    else:
                        print("No section header before this link:", line)
    return links_and_descriptions

def create_html(links_and_descriptions, output_filename="TxtToHtml.html"):
    html_content = '''<html>
<head>
    <title>TxtToHtml</title>
    <style>
        body, h1, h2, p, a, div {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #202020;
            color: #e0e0e0;
            padding: 40px;
            text-align: center;
        }

        .section-header {
            font-size: 2em;
            font-weight: bold;
            color: #bb86fc;
            text-transform: uppercase;
            margin-top: 30px;
            padding-bottom: 10px;
            text-align: center;
            border-bottom: 2px solid #bb86fc;
            width: 100%;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }

        .link-container {
            background-color: #282828;
            margin: 10px auto 30px;
            padding: 20px;
            border-radius: 8px;
            max-width: 900px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: box-shadow 0.3s ease;
        }

        .link-container:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .link-container a {
            display: block;
            color: #bb86fc;
            text-decoration: none;
            padding: 12px 20px;
            margin: 8px 0;
            border-radius: 4px;
            font-size: 1.1em;
            transition: background-color 0.3s, color 0.3s;
            text-align: left;
        }

        .link-container a:hover {
            background-color: #bb86fc;
            color: #121212;
        }

        .link-container img {
            width: 24px;
            height: 24px;
            margin-right: 10px;
            vertical-align: middle;
        }

        @media (max-width: 600px) {

            .section-header {
                font-size: 1.5em;
            }

            .link-container {
                padding: 15px;
            }

            .link-container a {
                font-size: 1em;
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    '''

    for section, links in links_and_descriptions:
        html_content += f'<div class="section-header">{section}</div>'
        html_content += '<div class="link-container">'
        
        for link, description in links:
            favicon_url = get_favicon_url(link)
            html_content += f'<a href="{link}" target="_blank"><img src="{favicon_url}" alt="Icon"> {description}</a>'
        
        html_content += '</div>'

    html_content += '''
</body>
</html>'''

    # Save the HTML content to a file
    with open(output_filename, 'w') as file:
        file.write(html_content)
    return output_filename

def open_in_chrome_incognito(html_filename):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Path to Chrome
    powershell_command = f"Start-Process '{chrome_path}' -ArgumentList '--incognito', '{os.path.abspath(html_filename)}'"
    subprocess.run(["powershell", "-Command", powershell_command])

if __name__ == "__main__":
    filename = 'TxtToHtml.txt'  # Name of your text file with links and descriptions
    links_and_descriptions = load_links_and_descriptions(filename)
    html_filename = create_html(links_and_descriptions)
    open_in_chrome_incognito(html_filename)