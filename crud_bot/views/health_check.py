from fastapi import APIRouter

healthcheck_route = APIRouter()


@healthcheck_route.get('/health')
async def health_check():
    return {'status': 'ok'}
