import uvicorn
from fastapi import FastAPI

# Это нужно для обозначения папки в которой нужно начинать
# отсчитывать абсолютный путь до файлов
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.config import settings

app = FastAPI()
app.include_router(hotels_router)



if __name__ == '__main__':
    # print(*hotels, sep="\n")
    uvicorn.run(app="main:app", port=8000, reload=True)
