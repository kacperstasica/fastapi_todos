from fastapi import HTTPException
from starlette import status


def http_exception():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
