import requests


def get_destination_urls(url : str, user_agent : str, referer : str) -> list[str]:
    with requests.Session() as session:
        session.headers.update({
            "User-Agent" : user_agent,
            "referer" : referer,
        })
        r = session.get(url)
        
        if r.status_code != 200:
            raise requests.exceptions.HTTPError(f"Invalid HTTP status: GET {url} --> {r.status_code}")
        
        dest_urls : list[str] = []
        
        if r.history:
            for step in r.history:
                dest_urls.append(step.url)
        
        dest_urls.append(r.url)
        
        return dest_urls[::-1]