from fastapi.responses import JSONResponse

def get_default_error_response(status_code=500,
                                     message="Internal Server Error"):
    """default error message template"""
    return JSONResponse(
        status_code=status_code,
        content={"status_code": status_code, "message": message},
    )
