from fastapi import FastAPI, status, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.config.settings import Settings
from src.routers.evaluator_router import router as evaluator_router
from src.routers.model_info_router import router as model_info_router
from src.routers.delete_router import router as delete_router
from src.routers.count_responses_router import router as count_responses_router
from src.routers.teacher_evaluation_router import router as teacher_eval_router
from src.config.db_config import engine, Base


settings = Settings()
app = FastAPI(title=settings.PROJECT_NAME)

Base.metadata.create_all(bind=engine)


app.include_router(evaluator_router, prefix="/evaluation", tags=["Evaluation"])
app.include_router(model_info_router, prefix="/model", tags=["ModelInfo"])
app.include_router(delete_router, prefix="/delete", tags=["Delete"])
app.include_router(
    count_responses_router, prefix="/count-responses", tags=["CountResponses"]
)
app.include_router(teacher_eval_router, prefix="/api", tags=["Teacher Evaluation"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
