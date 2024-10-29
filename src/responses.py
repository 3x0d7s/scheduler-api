import math

def paginated_response_content(result: list, page: int, size: int, count: int):
    total_pages = math.ceil(count / size)
    return {
        "result": result,
        "page": page,
        "totalPages": total_pages,
        "size": size,
        "count": count
    }
