from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dataManagement.database import engine
from dataManagement import models
from routers import country_routes, continent_routes
from auths import auth

# declares the start of the app. FastAPI handles this.
app = FastAPI()

# Fetches the model. If not possible then create a DB aligning to the required model.
models.Base.metadata.create_all(bind=engine)

# The routers to include.
app.include_router(country_routes.router)
app.include_router(continent_routes.router)
app.include_router(auth.router)

origins = [
    'http://localhost:3000'
]

# Permissions.
# everything is allowed at the moment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
