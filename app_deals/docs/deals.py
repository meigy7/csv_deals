from rest_framework import status
from drf_yasg import openapi

CATEGORY_ITEM = {
    "items": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(
                type=openapi.TYPE_INTEGER, example=1
            ),
            name=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            description=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            created_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            updated_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
        ),
    ),
}


UPLOAD_DEALS = {
    "operation_id": "Deal upload",
    "operation_description": """
        We can attach file to request and upload .csv file to server in order to analyze it.
    """,
    'manual_parameters': [
        openapi.Parameter('file', openapi.IN_QUERY,
                          description="Choose file with deals",
                          type=openapi.TYPE_FILE,
                          required=True),
        # openapi.Parameter('per_page', openapi.IN_QUERY,
        #                   description="Вы можете выбрать количество тематик на странице",
        #                   type=openapi.TYPE_NUMBER,
        #                   required=False),
    ],
    "responses": {
        status.HTTP_201_CREATED: openapi.Response(
            "Success",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    categories=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        **CATEGORY_ITEM
                    ),
                ),
            ),
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
          "Bad Request! Try again later"  
        )
    },
}


