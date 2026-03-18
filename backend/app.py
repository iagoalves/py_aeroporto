from fastapi import FastAPI
import models
from routers.aeroporto_routes import router as router_aeroporto
from routers.auth_routes import router as router_auth
from routers.reserva_routes import router as router_reserva


app = FastAPI()
app.include_router(router_aeroporto)
app.include_router(router_auth)
app.include_router(router_reserva)
