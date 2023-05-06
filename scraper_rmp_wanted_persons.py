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
                    "nama":         li.select_one("h3").get_text(strip=True, separator=" "),
                    "nama_gelaran": table_rows[1].select("td")[1].get_text(strip=True, separator=" "),
                    "no_kp":        table_rows[2].select("td")[1].get_text(strip=True, separator=" "),
                    "jantina":      table_rows[2].select("td")[3].get_text(strip=True, separator=" "),
                    "bangsa":       table_rows[3].select("td")[1].get_text(strip=True, separator=" "),
                    "tarikh_lahir": table_rows[3].select("td")[3].get_text(strip=True, separator=" "),
                    "alamat":       table_rows[4].select("td")[1].get_text(strip=True, separator=" "),
                    "repot_no":     table_rows[5].select("td")[1].get_text(strip=True, separator=" "),
                    "kesalahan":    table_rows[6].select("td")[1].get_text(strip=True, separator=" "),
                    "catatan":      table_rows[7].select("td")[1].get_text(strip=True, separator=" ").replace("\n", " "),
                    "photo":        urljoin(base_url, img_tag.get("src"))
            }
            
            results.append(result)
    
    file_name = "Royal_Malaysia_Police_Wanted_Persons_{0}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    field_names = ("nama", "nama_gelaran", "no_kp", "jantina", "bangsa", "tarikh_lahir", "alamat", "repot_no", "kesalahan", "catatan", "photo")
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
