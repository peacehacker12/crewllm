from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew

app = FastAPI()

class EmailData(BaseModel):
    from_: str
    subject: str
    body: str

@app.post("/generate-reply")
def generate_reply(data: EmailData):
    agent = Agent(
        role="Email Assistant",
        goal="Reply politely to incoming emails",
        backstory="You are a helpful assistant that writes polite and useful email replies.",
        verbose=True
    )

    task = Task(
        description=f"Reply to email:\nFrom: {data.from_}\nSubject: {data.subject}\nBody: {data.body}",
        expected_output="Write a short, helpful reply email.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    return {"reply": result}
