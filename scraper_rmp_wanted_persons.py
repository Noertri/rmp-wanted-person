from urllib.parse import urljoin
import csv
from datetime import datetime
import httpx
from bs4 import BeautifulSoup


def main():
    base_url = "https://www.rmp.gov.my"
    print("Scraping web...")
    client = httpx.Client()
    r = client.get(urljoin(base_url, "orang-dikehendaki"))
    
    results = list()
    if r.status_code == 200:
        souped = BeautifulSoup(r.content, "html.parser")
        litags = souped.select_one("ul.sflistList").select("li")
        
        for li in litags:
            img_tag = li.select_one("img")
            table_rows = li.select_one("table").select("tr")
            
            result = {
                    "name":         li.select_one("h3").get_text(strip=True, separator=" "),
                    "nickname": table_rows[1].select("td")[1].get_text(strip=True, separator=" "),
                    "id_number":        table_rows[2].select("td")[1].get_text(strip=True, separator=" "),
                    "gender":      table_rows[2].select("td")[3].get_text(strip=True, separator=" "),
                    "nation":       table_rows[3].select("td")[1].get_text(strip=True, separator=" "),
                    "date_of_birth": table_rows[3].select("td")[3].get_text(strip=True, separator=" "),
                    "address":       table_rows[4].select("td")[1].get_text(strip=True, separator=" "),
                    "report_no":     table_rows[5].select("td")[1].get_text(strip=True, separator=" "),
                    "case":    table_rows[6].select("td")[1].get_text(strip=True, separator=" "),
                    "notes":      table_rows[7].select("td")[1].get_text(strip=True, separator=" ").replace("\n", " "),
                    "link_photo":        urljoin(base_url, img_tag.get("src"))
            }
            
            results.append(result)
    
    file_name = "Royal_Malaysia_Police_Wanted_Persons_{0}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    field_names = ("name", "nickname", "id_number", "gender", "nation", "date_of_birth", "address", "report_no", "case", "notes", "link_photo")
    print(f"Save to {file_name}...")
    try:
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=field_names, delimiter=";")
            writer.writeheader()
            writer.writerows(results)
            f.close()
        print("Done..")
    except Exception as e:
        print(f"Error: {e}")
    

if __name__ == "__main__":
    main()
