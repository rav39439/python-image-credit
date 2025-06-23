# def greet(name):
#     print(f"Hello, {name}!")

# if __name__ == "__main__":
#     greet("VS Code User")

from fastapi import FastAPI
from Routes import task_routes  # Import the router
from Routes import user_routes  # Import the router
from fastapi.middleware.cors import CORSMiddleware

from Routes import transactions  # Import the router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://next-js-app-ochre-iota.vercel.app",
        "https://your-production-domain.com",
    ],
    allow_credentials=True,            # allow cookies, Authorization headers
    allow_methods=["*"],               # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],               # allow all headers
)

# Include the routes from task_routes
app.include_router(task_routes.router)

app.include_router(user_routes.router)

app.include_router(transactions.router)
