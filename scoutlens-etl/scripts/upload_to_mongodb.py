import pandas as pd
from pymongo import MongoClient
import os
import json
import numpy as np
import pycountry
from bson import ObjectId
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def load_data(input_file: str) -> pd.DataFrame:
    """Load JSON data into DataFrame"""
    with open(input_file, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)


def rename_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Transform field names using mapping"""
    field_mapping = {
        "Rk": "rank",
        "Player": "fullName",
        "Nation": "nation",
        "Pos": "position",
        "Squad": "team",
        "Comp": "league",
        "Age": "age",
        "Born": "yearOfBirth",
        "MP": "matchesPlayed",
        "Starts": "matchesStarted",
        "Min": "minutesPlayed",
        "90s": "minutesPer90",
        "Goals": "goalsScored",
        "Shots": "totalShots",
        "SoT": "shotsOnTarget",
        "SoT%": "shotsOnTargetPercentage",
        "G/Sh": "goalsPerShot",
        "G/SoT": "goalsPerShotOnTarget",
        "ShoDist": "averageShotDistance",
        "ShoFK": "shotsFromFreeKicks",
        "ShoPK": "penaltyKicksMade",
        "PKatt": "penaltyKicksAttempted",
        "PasTotCmp": "totalPassesCompleted",
        "PasTotAtt": "totalPassesAttempted",
        "PasTotCmp%": "passCompletionPercentage",
        "PasTotDist": "totalPassDistance",
        "PasTotPrgDist": "totalProgressivePassDistance",
        "PasShoCmp": "shortPassesCompleted",
        "PasShoAtt": "shortPassesAttempted",
        "PasShoCmp%": "shortPassCompletionPercentage",
        "PasMedCmp": "mediumPassesCompleted",
        "PasMedAtt": "mediumPassesAttempted",
        "PasMedCmp%": "mediumPassCompletionPercentage",
        "PasLonCmp": "longPassesCompleted",
        "PasLonAtt": "longPassesAttempted",
        "PasLonCmp%": "longPassCompletionPercentage",
        "Assists": "assists",
        "PasAss": "passesLeadingToShot",
        "Pas3rd": "passesIntoFinalThird",
        "PPA": "passesIntoPenaltyArea",
        "CrsPA": "crossesIntoPenaltyArea",
        "PasProg": "progressivePasses",
        "PasAtt": "passesAttempted",
        "PasLive": "livePasses",
        "PasDead": "deadPasses",
        "PasFK": "freeKickPasses",
        "TB": "throughBalls",
        "Sw": "switches",
        "PasCrs": "PassToCrosses",
        "TI": "throwIns",
        "CK": "cornerKicks",
        "CkIn": "inswingingCornerKicks",
        "CkOut": "outswingingCornerKicks",
        "CkStr": "straightCornerKicks",
        "PasCmp": "passesCompleted",
        "PasOff": "PassToOffsides",
        "PasBlocks": "passesBlocked",
        "SCA": "shotCreatingActions",
        "ScaPassLive": "shotCreatingPassesLive",
        "ScaPassDead": "shotCreatingPassesDead",
        "ScaDrib": "shotCreatingDribbles",
        "ScaSh": "shotCreatingShots",
        "ScaFld": "shotCreatingFoulsDrawn",
        "ScaDef": "shotCreatingDefensiveActions",
        "GCA": "goalCreatingActions",
        "GcaPassLive": "goalCreatingPassesLive",
        "GcaPassDead": "goalCreatingPassesDead",
        "GcaSh": "goalCreatingShots",
        "GcaFld": "goalCreatingFoulsDrawn",
        "GcaDef": "goalCreatingDefensiveActions",
        "Tkl": "tackles",
        "TklWon": "tacklesWon",
        "TklDef3rd": "tacklesInDefensiveThird",
        "TklMid3rd": "tacklesInMiddleThird",
        "TklAtt3rd": "tacklesInAttackingThird",
        "TklDri": "dribblersTackled",
        "TklDriAtt": "dribblesAttempted",
        "TklDri%": "percentageDribblersTackled",
        "TklDriPast": "timesDribbledPast",
        "Blocks": "blocks",
        "BlkSh": "shotsBlocked",
        "BlkPass": "blockedPasses",
        "Int": "interceptions",
        "Tkl+Int": "tacklesAndInterceptions",
        "Clr": "clearances",
        "Err": "errorsLeadingToShot",
        "Touches": "touches",
        "TouDefPen": "touchesInDefensivePenaltyArea",
        "TouDef3rd": "touchesInDefensiveThird",
        "TouMid3rd": "touchesInMiddleThird",
        "TouAtt3rd": "touchesInAttackingThird",
        "TouAttPen": "touchesInAttackingPenaltyArea",
        "TouLive": "liveBallTouches",
        "ToAtt": "takeOnAttempts",
        "ToSuc": "takeOnSuccesses",
        "ToSuc%": "takeOnSuccessPercentage",
        "ToTkl": "timesTackled",
        "ToTkl%": "tacklePercentage",
        "Carries": "carries",
        "CarTotDist": "totalCarryDistance",
        "CarPrgDist": "progressiveCarryDistance",
        "CarProg": "progressiveCarries",
        "Car3rd": "carriesIntoFinalThird",
        "CPA": "carriesIntoPenaltyArea",
        "CarMis": "miscontrols",
        "CarDis": "dispossessions",
        "Rec": "passesReceived",
        "RecProg": "progressivePassesReceived",
        "CrdY": "yellowCards",
        "CrdR": "redCards",
        "2CrdY": "secondYellowCards",
        "Fls": "foulsCommitted",
        "Fld": "foulsDrawn",
        "Off": "offsides",
        "Crs": "crosses",
        "TklW": "tacklesWonPercentage",
        "PKwon": "penaltyKicksWon",
        "PKcon": "penaltyKicksConceded",
        "OG": "ownGoals",
        "Recov": "ballRecoveries",
        "AerWon": "aerialDuelsWon",
        "AerLost": "aerialDuelsLost",
        "AerWon%": "aerialDuelsWonPercentage",
    }
    return df.rename(columns=field_mapping)


def normalize_country_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert country codes/names to full country names"""

    # Custom mapping for common football nationalities that might not be in pycountry
    custom_country_mapping = {
        "ALG": "Algeria",
        "ANG": "Angola",
        "BUL": "Bulgaria",
        "CGO": "Congo",
        "CHI": "Chile",
        "CRC": "Costa Rica",
        "CRO": "Croatia",
        "CTA": "Central African Republic",
        "DEN": "Denmark",
        "ENG": "United Kingdom",
        "EQG": "Equatorial Guinea",
        "GAM": "Gambia",
        "GER": "Germany",
        "GRE": "Greece",
        "GRN": "Grenada",
        "GUI": "Guinea",
        "HAI": "Haiti",
        "HON": "Honduras",
        "KVX": "Kosovo",
        "MAD": "Madagascar",
        "NED": "Netherlands",
        "NIR": "Northern Ireland",
        "PAR": "Paraguay",
        "POR": "Portugal",
        "PHI": "Philippines",
        "RSA": "Saudi Arabia",
        "SCO": "Scotland",
        "SUI": "Switzerland",
        "TOG": "Togo",
        "URU": "Uruguay",
        "USA": "United States of America",
        "WAL": "Wales",
        "ZAM": "Zambia",
        "ZIM": "Zimbabwe",
    }

    def get_full_country_name(country_code: str) -> str:
        # Check custom mapping first
        if country_code in custom_country_mapping:
            return custom_country_mapping[country_code]

        try:
            # Try to find by alpha_3 (three-letter code)
            country = pycountry.countries.get(alpha_3=country_code)
            if country:
                return country.name

            # Try to find by alpha_2 (two-letter code)
            country = pycountry.countries.get(alpha_2=country_code)
            if country:
                return country.name

            # Try to find by name
            country = pycountry.countries.get(name=country_code)
            if country:
                return country.name

            return country_code  # Return original if not found

        except (AttributeError, LookupError):
            return country_code

    df["nation"] = df["nation"].apply(get_full_country_name)
    return df


def calculate_basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate basic performance statistics"""
    # Goal contributions
    df["goalContributions"] = df["goalsScored"] + df["assists"]

    # Minutes per goal contribution
    df["minutesPerGoalContribution"] = df["minutesPlayed"] / (
        df["goalContributions"].replace(0, np.nan)
    )
    df["minutesPerGoalContribution"] = df["minutesPerGoalContribution"].fillna(0)

    # Per 90 minutes stats
    df["goalsPerNinety"] = (
        df["goalsScored"] * 90 / df["minutesPlayed"].replace(0, np.nan)
    )
    df["assistsPerNinety"] = df["assists"] * 90 / df["minutesPlayed"].replace(0, np.nan)

    # Fill NaN values
    df["goalsPerNinety"] = df["goalsPerNinety"].fillna(0)
    df["assistsPerNinety"] = df["assistsPerNinety"].fillna(0)

    return df


def calculate_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate percentage-based statistics"""
    # Games started percentage
    df["gamesStartedPercentage"] = (
        df["matchesStarted"] / df["matchesPlayed"] * 100
    ).round(2)

    # Shot conversion rate
    df["shotConversionRate"] = (df["goalsScored"] / df["totalShots"] * 100).round(2)
    df["shotConversionRate"] = df["shotConversionRate"].fillna(0)

    return df


def round_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    """Round all numeric values to 2 decimal places"""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].round(2)
    return df


def normalize_positions(df: pd.DataFrame) -> pd.DataFrame:
    """Convert position codes to their specific full position names"""

    # Specific position mapping as provided
    position_mapping = {
        "DF": "Defender",
        "DFFW": "Fullback",
        "DFMF": "Defensive Midfielder",
        "FW": "Attacker",
        "FWDF": "Attacking Midfielder",
        "FWMF": "Wide Midfielder",
        "GK": "Goalkeeper",
        "MF": "Midfielder",
        "MFDF": "Defensive Midfielder",
        "MFFW": "Winger",
    }

    # Apply the transformation
    position_column = "position" if "position" in df.columns else "Pos"
    df[position_column] = df[position_column].map(position_mapping).fillna("Unknown")

    return df


def save_data(df: pd.DataFrame, output_file: str):
    """Save processed data to JSON file"""
    processed_data = df.to_dict("records")
    with open(output_file, "w") as f:
        json.dump(processed_data, f, indent=2)


def print_summary(df: pd.DataFrame):
    """Print basic summary statistics"""
    print("\nData Summary:")
    print(f"Total players processed: {len(df)}")
    print(f"Number of leagues: {df['league'].nunique()}")
    print(f"Number of teams: {df['team'].nunique()}")
    print(f"Number of nationalities: {df['nation'].nunique()}")

    print("\nTop 5 Goal Scorers:")
    print(
        df.nlargest(5, "goalsScored")[
            ["fullName", "team", "nation", "goalsScored", "goalsPerNinety"]
        ]
    )

    print("\nTop 5 Assist Providers:")
    print(
        df.nlargest(5, "assists")[
            ["fullName", "team", "nation", "assists", "assistsPerNinety"]
        ]
    )

    print("\nMost Represented Countries:")
    print(df["nation"].value_counts().head())


def process_dataset(input_file: str):
    """Main processing pipeline"""
    # Load data
    df = load_data(input_file)

    # Transform field names
    df = rename_fields(df)

    # Normalize country names
    df = normalize_country_names(df)

    # Normalize positions with new mapping
    df = normalize_positions(df)

    # Calculate statistics
    df = calculate_basic_stats(df)
    df = calculate_percentages(df)

    # Round numeric values
    df = round_numeric_values(df)

    return df


def connect_mongodb():
    # Connect to MongoDB
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_port = int(os.getenv("MONGO_PORT", "27018"))
    mongo_user = os.getenv("MONGO_USER", "scoutlens_admin")
    mongo_password = os.getenv("MONGO_PASSWORD", "password")
    mongo_db = os.getenv("MONGO_DB", "scoutlens")
    mongo_collection = os.getenv("MONGO_COLLECTION", "players")

    # Construct the MongoDB URI with authentication
    mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]
    return collection


def rename_id_field(doc):
    """Helper function to rename _id to mid in a document"""
    if "_id" in doc:
        doc["mid"] = doc.pop("_id")
    return doc


def persist_data(data):
    collection = connect_mongodb()

    # Convert DataFrame to dictionary and insert into MongoDB
    data_dict = data.to_dict("records")
    try:
        collection.insert_many(data_dict)
        print("Data successfully inserted into MongoDB.")
    except Exception as e:
        print(f"Failed to insert data: {e}")


def export_data(output_file):
    try:
        collection = connect_mongodb()
        documents = list(collection.find())

        # Rename _id to m_id in all documents
        documents = [rename_id_field(doc) for doc in documents]

        # Create output directory if it doesn't exist
        os.makedirs(
            os.path.dirname(output_file) if os.path.dirname(output_file) else ".",
            exist_ok=True,
        )

        # Write to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(documents, f, cls=JSONEncoder, ensure_ascii=False, indent=2)

        print(f"Successfully exported {len(documents)} documents to {output_file}")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    export_data("./dataset/mongo-players-data.json")
