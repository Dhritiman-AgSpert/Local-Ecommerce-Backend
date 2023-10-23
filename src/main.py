from fastapi import FastAPI
from .apis.auth import router as auth_api_router
from .apis.categories import router as categories_api_router
from .apis.address import router as address_api_router
from .apis.upload import router as upload_api_router
from .apis.product import router as product_api_router
from .apis.payment import router as payment_api_router

 
def create_app():
    """ Factory function for creating an app instance """
    app = FastAPI(
        title="AgVefr Backend Documentation",
        description="Enhancing the ease of selling and buying.",
        summary="Documentation of Backend for AgVefr",
        version="0.0.1",
        terms_of_service="http://example.com/terms/",
        contact={
            "name": "Dhritiman Talukdar",
            "url": "https://www.linkedin.com/in/dhritiman-talukdar-76a745122/",
            "email": "dhritimant@gmail.com",
        }
    )
    register_routers(app)
    return app


def register_routers(app: FastAPI):
    """ Router includes go here """
    app.include_router(auth_api_router, prefix="/auth", tags=["auth"])
    app.include_router(categories_api_router, prefix="/categories", tags=["categories"])
    app.include_router(address_api_router, prefix="/address", tags=["address"])
    app.include_router(upload_api_router, prefix="/upload", tags=["upload"])
    app.include_router(product_api_router, prefix="/product", tags=["product"])
    app.include_router(payment_api_router, prefix="/payment", tags=["payment"])

app = create_app()