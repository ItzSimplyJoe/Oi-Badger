import requests
class WebAnswers:
    def search_google_api(self, query, api_key, cx):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cx,
            "q": query
        }
        response = requests.get(url, params=params)
        return response.json()

    def extract_top_result(self, response):
        items = response.get("items", [])
        if items:
            top_result = items[0]
            title = top_result.get("title")
            link = top_result.get("link")
            snippet = top_result.get("snippet")
            return {
                "title": title,
                "link": link,
                "snippet": snippet
            }
        return None

    def get_answer(self, query):
        with open("Functions/webanswers/googleapi.key", "r") as file:
            api_key = file.read()
            file.close()
        with open("Functions/webanswers/googlecx.key", "r") as file:
            cx = file.read()
            file.close()
        response = self.search_google_api(query, api_key, cx)
        result = self.extract_top_result(response)
        if result:
            print("Title:", result["title"])
            print("Link:", result["link"])
            print("Snippet:", result["snippet"])
        else:
            print("No results found.")

webanswers = WebAnswers()

