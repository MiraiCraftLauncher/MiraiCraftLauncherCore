from bs4 import BeautifulSoup

forge_official = "https://files.minecraftforge.net/net/minecraftforge/forge/index_%v.html"

bmclapi = "https://bmclapi2.bangbang93.com/forge/minecraft/%v"

"""
async def get_version(version:str):
    
    versions = {}
    soup = BeautifulSoup(html_content,"html.parser")
    html_obj = soup.find("tbody")
    for tr in html_obj.children:
        for td in tr.find_all_next("td"):
            attrs = td.attrs.get("class")
            if "download-version" in attrs:
"""