from barbershopp.settings import MISTRAL_MODERATIONS_GRADES
import os
from dottenv import load_dotenv
from mistralai import Mistral
from pprint import pprint
load_dotenv()

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def moderate_review(review_text: str, api_key: str = MISTRAL_API_KEY, grades: dict = MISTRAL_MODERATIONS_GRADES) -> bool:
    client = Mistral(api_key=api_key)
    response = client.classifiers.moderate_chat(
        model = "mistral-moderation-latest",
        inputs = [
            { "role": "user", "content": review_text},
        ],
    )
    result = response.results[0].category_scores
    result = {key: round(value, 2) for key, value in raw_result.items()}

    pprint(result)

    cheked_result = {}
    for key, value in result.items():
        if key in grades:
            cheked_result[key] = value >= grades[key]
    return all(cheked_result.values())