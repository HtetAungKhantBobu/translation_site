from drf_yasg import openapi

Q = openapi.Parameter(
    "q",
    openapi.IN_QUERY,
    description="Search Query",
    required=False,
    type=openapi.TYPE_STRING,
)

SORT = openapi.Parameter(
    "sort",
    openapi.IN_QUERY,
    description="Sort Query",
    required=False,
    type=openapi.TYPE_STRING,
)

ASC = openapi.Parameter(
    "asc",
    openapi.IN_QUERY,
    description="Ascending or Descending Sorting Query",
    required=False,
    type=openapi.TYPE_BOOLEAN,
    default=True,
)
