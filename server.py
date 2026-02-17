from mcp.server.fastmcp import FastMCP
from cube_client import CubeClient
import os
import sys
from dotenv import load_dotenv

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load .env from the bundled path if available
load_dotenv(resource_path(".env"))


CUBE_URL = "https://88684694-fc0a-4ce6-afc7-deb10668883d-4000.tenants.hivecompute.ai/cubejs-api/v1"
SECRET = os.getenv("CUBEJS_API_SECRET")

if not SECRET:
    # If still not found, check standard location as fallback
    load_dotenv() 
    SECRET = os.getenv("CUBEJS_API_SECRET")

if not SECRET:
    cube = CubeClient(CUBE_URL, "MISSING_SECRET")
else:
    cube = CubeClient(CUBE_URL, SECRET)

mcp = FastMCP(
    name="hivenet-analytics",
)

@mcp.tool()
def get_cube_meta():
    """Get available cubes, measures, dimensions, and time dimensions."""
    meta = cube.get_meta()

    cubes = []
    for c in meta.get("cubes", []):
        cubes.append({
            "name": c["name"],
            "measures": [m["name"] for m in c.get("measures", [])],
            "dimensions": [d["name"] for d in c.get("dimensions", [])],
            "timeDimensions": [
                d["name"] for d in c.get("dimensions", [])
                if d.get("type") == "time"
            ]
        })

    return {"cubes": cubes}


@mcp.tool()
def run_cube_query(
    measures: list[str],
    dimensions: list[str] | None = None,
    time_dimension: str | None = None,
    date_range: list[str] | None = None,
    limit: int | None = None
):
    query = {
        "measures": measures,
        "dimensions": dimensions or []
    }

    if time_dimension and date_range:
        query["timeDimensions"] = [{
            "dimension": time_dimension,
            "dateRange": date_range
        }]

    if limit:
        query["limit"] = limit

    result = cube.run_query({
        "query": query
    })

    return result.get("data", [])


import asyncio
if __name__ == "__main__":
    asyncio.run(mcp.run())
