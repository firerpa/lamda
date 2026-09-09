#!/usr/bin/env python3
# THIS IS EXAMPLE HTTP OCR BACKEND,
#     DO NOT USE IN PRODUCTION
import uvicorn
import asyncio
import paddle as paddle
from paddleocr import PaddleOCR
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/ocr")
async def ocr(request: Request):
    image = await request.body()
    r = await asyncio.to_thread(ocr.ocr, image)
    n = bool(r and r[0] and type(r[0][-1])==float)
    result = (r if n else r[0]) or []
    output = [[n[0], n[1][0], n[1][1]] for n in result]
    return output


if __name__ == "__main__":
    ocr = PaddleOCR(use_gpu=False, drop_score=0.85,
                            use_space_char=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)