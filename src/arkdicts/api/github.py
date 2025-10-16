import requests
from typing import Dict, List, Optional


def send_request(
    method: str, url: str, token: str, data: Optional[Dict] = None
) -> requests.Response:
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.request(
        method=method, url=url, headers=headers, json=data, timeout=30
    )
    return response


def get_all_labels(owner: str, repo: str, token: str) -> Optional[List]:
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    response = send_request("GET", url, token)
    all_data = response.json()

    while "next" in response.links:
        next_url = response.links["next"]["url"]
        response = send_request("GET", next_url, token)
        all_data.extend(response.json())

    if response.status_code != 200:
        return None
    return all_data


def add_label(
    owner: str,
    repo: str,
    token: str,
    label_name: str,
    color: str,
    description: Optional[str] = None,
) -> bool:
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    data = {
        "name": label_name,
        "color": color.replace("#", ""),
    }
    if description:
        data["description"] = description
    response = send_request("POST", url, token, data)
    if response.status_code != 201:
        return False
    return True


def delete_label(owner: str, repo: str, token: str, label_name: str) -> bool:
    from urllib.parse import quote

    encoded_label_name = quote(label_name)

    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{encoded_label_name}"

    response = send_request("DELETE", url, token)

    if response.status_code != 204:
        return False
    return True

