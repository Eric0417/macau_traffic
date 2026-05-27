from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# 允許所有來源連線 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存在記憶體中的全域變數，用來暫存最新的路況數據
traffic_data = {"type": "FeatureCollection", "features": []}

# 1. 網頁端點：當使用者在瀏覽器輸入網址時，給他 index.html
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

# 2. 前端索取端點：網頁每 5 秒會來這裡拿最新數據
@app.get("/api/traffic")
def get_traffic_data():
    return traffic_data

# 3. AI 接收端點：v2_detector.py 每 5 秒推送 GeoJSON
@app.post("/api/update")
async def update_traffic_data(request: Request):
    global traffic_data
    try:
        data = await request.json()
        features = data.get("features", [])
        cameras = [f for f in features if f.get("properties", {}).get("type") == "camera"]
        streets = [f for f in features if f.get("properties", {}).get("type") == "street"]
        traffic_data = data
        print(f"收到數據: {len(cameras)} 攝影機, {len(streets)} 路段, 更新時間 {data.get('last_updated', '?')}")
        return {"status": "success", "cameras": len(cameras), "streets": len(streets)}
    except Exception as e:
        print(f"接收錯誤: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)