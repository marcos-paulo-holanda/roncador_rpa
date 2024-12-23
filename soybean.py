import requests
from bs4 import BeautifulSoup

def search_soybean_price_influences():
    query = "fatores recentes que influenciam o preco da soja"
    search_url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # Make the request
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find search results
        results = []
        for g in soup.find_all("div", class_="tF2Cxc"):
            title = g.find("h3").text
            link = g.find("a")["href"]
            snippet = g.find("span", class_="aCOpRe").text
            results.append({"title": title, "link": link, "snippet": snippet})

        # Display results
        if results:
            print("Resultados encontrados:")
            for idx, result in enumerate(results):
                print(f"\n{idx + 1}. {result['title']}")
                print(f"Link: {result['link']}")
                print(f"Resumo: {result['snippet']}")
        else:
            print("Nenhum resultado encontrado.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao realizar a busca: {e}")

if __name__ == "__main__":
    search_soybean_price_influences()
