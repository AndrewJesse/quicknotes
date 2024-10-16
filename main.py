from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import asyncio
import httpx

app = FastAPI()

"""             +-------------------------------------------------------+
CMD To Run ->   | uvicorn main:app --host 0.0.0.0 --port 8000 --reload\ |
Main Endpoint ->|  http://localhost:8000                                |
Swagger UI ->   |  http://localhost:8000/docs                           |
ReDoc ->        |  http://localhost:8000/redoc                          |
                +-------------------------------------------------------+"""

@app.get("/", response_class=HTMLResponse)  # http://localhost:8000
def read_boot():
    html_content = """
    <html>
        <head>
            <title>FastAPI Example</title>
        </head>
        <body>
            <h1>Welcome to FastAPI</h1>
            <button onclick="fetchData('numbers')">Get Numbers</button>
            <button onclick="fetchData('joke')">Get Joke</button>
            <div id="result"></div>
            <script>
                async function fetchData(type) {
                    const response = await fetch(`/numbers?type=${type}`);
                    const data = await response.json();
                    document.getElementById('result').innerText = JSON.stringify(data, null, 2);
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/numbers")  # http://localhost:8000/numbers
async def read_numbers(type: str = "joke"):
    if type == "numbers":
        await asyncio.sleep(2)
        return {"numbers": [1, 2, 3, 4, 5]}
    elif type == "joke":
        url = "https://official-joke-api.appspot.com/random_joke"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching joke")
            joke = response.json()
            return {"setup": joke["setup"], "punchline": joke["punchline"]}
    else:
        raise HTTPException(status_code=400, detail="Invalid type parameter")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)