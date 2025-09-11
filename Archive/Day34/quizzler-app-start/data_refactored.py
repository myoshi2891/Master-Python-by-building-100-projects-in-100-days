from typing import Any, Dict, List
import requests


def get_question_data(amount: int = 10, q_type: str = "boolean") -> List[Dict[str, Any]]:
    """
    Open Trivia DB API からクイズ問題を取得する。

    Args:
        amount (int): 取得する問題数
        q_type (str): 問題の種類 ("boolean", "multiple" など)

    Returns:
        List[Dict[str, Any]]: クイズ問題データのリスト
    """
    url = "https://opentdb.com/api.php"
    params: Dict[str, str | int] = {
        "amount": amount,
        "type": q_type,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data: Dict[str, Any] = response.json()
    return data.get("results", [])
