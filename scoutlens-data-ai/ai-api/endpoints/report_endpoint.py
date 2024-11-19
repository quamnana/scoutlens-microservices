from fastapi import APIRouter, HTTPException, Request
from datetime import datetime
from services.report_service import report_service
from services.mongodb_service import mongo_service


router = APIRouter(prefix="/generate_report", tags=["generate_report"])


@router.post("/")
async def generate_report(request: Request):
    try:
        # Extract JSON data from the request
        player_data = await request.json()

        # Check if the report already exists in MongoDB
        existing_report = mongo_service.get_report_by_rank(
            player_data.get("rank", None)
        )

        if existing_report:
            return {
                "report": existing_report["generated_report"],
            }

        # Call the service method to generate the report
        generated_report = report_service.get_scouting_report(player_data)

        # Save the report to MongoDB
        report_data = {
            "rank": player_data.get("rank", None),
            "fullName": player_data.get("fullName", None),
            "generated_report": generated_report,
        }

        mongo_service.save_report_to_db(report_data)

        return {"report": generated_report}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid input data.")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the report. {e}",
        )
