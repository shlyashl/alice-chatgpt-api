import os
from time import sleep
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import openai
from dotenv import load_dotenv

load_dotenv()


class GPTSessions:
    def __init__(self):
        self.answers = {}
        openai.api_key = os.getenv('OAI_TOKEN')

    def create_gpt_answer(self, session_id: str, promt: str):
        self.answers[session_id] = 'Created'
        completion = openai.Completion.create(engine='text-davinci-003', prompt=promt, max_tokens=1024, n=1,
                                              stop=None, temperature=0.6)
        self.answers[session_id] = completion.choices[0].text

    def get_gpt_answer(self, session_id: str):
        return self.answers.get(session_id)

    def forget_session(self, session_id: str):
        if self.answers.get(session_id):
            self.answers.pop(session_id)


app = FastAPI()
sessions = GPTSessions()


@app.post("/api/alice")
async def root(request: Request, background_tasks: BackgroundTasks, answer='Привет!'):
    request = await request.json()
    promt = request['request']['original_utterance']
    session_id = request['session']['session_id']
    response = {'session': request['session'], 'version': request['version'],
                'response': {'end_session': False}}

    if promt and not sessions.get_gpt_answer(session_id):
        background_tasks.add_task(sessions.create_gpt_answer, session_id, promt)
        for i in range(25):
            if sessions.get_gpt_answer(session_id):
                break
            else:
                sleep(0.1)
        answer = 'Вернись попозже.'

    elif sessions.get_gpt_answer(session_id) == 'Created':
        answer = 'Нужно еще время, вернись попозже.'
    elif sessions.get_gpt_answer(session_id):
        answer = sessions.get_gpt_answer(session_id)
        sessions.forget_session(session_id)
    elif not promt:
        pass
    else:
        sessions.forget_session(session_id)
    response['response']['text'] = answer
    return response


if __name__ == "__main__":
    port = int(os.getenv('API_PORT'))
    uvicorn.run("main:app", port=port, log_level="info")
