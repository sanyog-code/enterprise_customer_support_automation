from fastapi import FastAPI
from pydantic import BaseModel
import time
from src.support_bot.crew import SupportBotCrew
 
app = FastAPI()
 
class Query(BaseModel):
    query: str
 
@app.post("/query")
async def handle_query(request: Query):
    start = time.time()
    # Injecting your name into the pipeline context
    inputs = {'query': request.query, 'user_name': 'Shreesanyog Rath'}
    result = SupportBotCrew().crew().kickoff(inputs=inputs)
    
    return {
        "status": "success",
        "response": str(result),
        "execution_time": f"{round(time.time() - start, 2)}s"
    }
 