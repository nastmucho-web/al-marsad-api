from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from moroccan_hilal_checker import MoroccanHilalChecker
from datetime import datetime

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

checker = MoroccanHilalChecker()

# المدن
CITIES = [
    "Ceuta",   # الشمال
    "Tangier",
    "Lagouira",  # الجنوب
    "Laayoune",
    "Figuig",     # الشرق
    "Oujda",
    "Rabat",     # الغرب
    "Casablanca"
]
def get_day_name(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    days = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    return days[date_obj.weekday()]

@app.get("/predict")
def predict(type: str, year: int = 1447, city: str = "Tangier"):

    if type == "ramadan":
        month = "Ramadan"
        label = "أول أيام رمضان سيكون يوم"

    elif type == "fitr":
        month = "Shawwal"
        label = "عيد الفطر سيكون يوم"

    elif type == "adha":
        month = "Dhu al-Hijjah"
        label = "عيد الأضحى سيكون يوم"

    else:
        return {"result": "خطأ"}

    try:
        y, m, d, prob = checker.get_miladi_day_for_hilal(
            year,
            month,
            probability_threshold=0.8
        )

        from datetime import datetime

        date_obj = datetime(y, m, d)

        days_ar = [
            "الاثنين", "الثلاثاء", "الأربعاء",
            "الخميس", "الجمعة", "السبت", "الأحد"
        ]

        day_name = days_ar[date_obj.weekday()]

        date_str = f"{y}-{m:02d}-{d:02d}"

        result = f"{label} {day_name} {date_str}\nوالله أعلى وأعلم"

    except Exception as e:
        result = f"وقع خطأ: {str(e)}"

    return JSONResponse(
        content={"result": result},
        media_type="application/json; charset=utf-8"
    )