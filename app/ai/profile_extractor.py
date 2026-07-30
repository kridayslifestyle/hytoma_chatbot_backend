import json

from app.ai.llm_service import client


def extract_profile(message: str):

    response = client.chat.completions.create(

        model="deepseek/deepseek-chat-v3-0324",

        messages=[

            {
                "role": "system",

                "content": """
Extract customer preferences.

Return ONLY valid JSON.

Example:

{
    "budget":"50000",
    "preferred_color":"Black",
    "ecosystem":"Alexa",
    "interests":[],
    "location":"Hyderabad"
}

Do not explain anything.
Do not add markdown.
Return JSON only.
"""
            },

            {
                "role": "user",
                "content": message
            }

        ]

    )

    content = response.choices[0].message.content

    print("\nRAW RESPONSE:")
    print(content)

    # Remove markdown code blocks
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:

        return json.loads(content)

    except Exception as e:

        print("\nJSON ERROR:")
        print(e)

        return {}