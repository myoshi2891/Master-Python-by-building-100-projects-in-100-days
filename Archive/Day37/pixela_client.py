import requests
from requests import Response
from datetime import datetime

PIXELA_URL = "https://pixe.la/v1/users"


def create_pixel(token: str, username: str, graph_id: str, date: datetime, quantity: str) -> Response:
    """指定した日付に学習時間を記録する"""
    pixel_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}"
    pixel_data = {
        "date": date.strftime("%Y%m%d"),
        "quantity": quantity,
    }
    headers = {"X-USER-TOKEN": token}
    return requests.post(url=pixel_endpoint, json=pixel_data, headers=headers)


def update_pixel(token: str, username: str, graph_id: str, date: datetime, quantity: str) -> Response:
    """指定した日付の学習時間を更新する"""
    update_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}/{date.strftime('%Y%m%d')}"
    pixel_update_data = {"quantity": quantity}
    headers = {"X-USER-TOKEN": token}
    return requests.put(url=update_endpoint, json=pixel_update_data, headers=headers)


def delete_pixel(token: str, username: str, graph_id: str, date: datetime) -> Response:
    """指定した日付の学習時間を削除する"""
    delete_endpoint = f"{PIXELA_URL}/{username}/graphs/{graph_id}/{date.strftime('%Y%m%d')}"
    headers = {"X-USER-TOKEN": token}
    return requests.delete(url=delete_endpoint, headers=headers)
