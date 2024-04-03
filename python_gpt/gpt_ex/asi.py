from openai import OpenAI
import re
import json
api_key=""
client = OpenAI(api_key=api_key)

assistant = client.beta.assistants.create(
    name="ActivityGenerator",
    instructions="주간 일정을 입력 받아서 남은 여가 시간을 무엇을 할지 추천해주는 어시스턴스야 입력은 다음과 같아  ```월':9:00 ~ 18:00=수업, 18:30~19:30=요가 ``` 남은 시간에 대해서 좋은 활동과 시간을 추천해줘",
    tools=[{"type": "code_interpreter"}],
    # model="gpt-4-turbo-preview",
    model="gpt-3.5-turbo-1106",
)
# 생성된 어시스턴트의 ID를 추출합니다.
print("id:", assistant.id)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="월':9:00 ~ 18:00=수업, 18:30~19:30=요가 다른 활동은 어떤걸 하면 좋을까?"
)
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)
# 만들고 나서
# run = client.beta.threads.runs.create(
#   thread_id=thread.id,
#   assistant_id="asst_86wgOJ0IVka5gLcPMwf80VoB",
#   instructions="Please address the user as Jane Doe. The user has a premium account."
# )
#

import time

while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1)  # Wait for 1 second
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        # print(messages)
        # Extract the message content
        message_content = messages.data[0].content[0].text
        # print(message_content.value)
        # 텍스트를 분리하고, 각 항목을 파싱하여 JSON 형식의 딕셔너리로 변환합니다.
        activities = []
        activities_dic = {}
        current_activity = ""

        for line in message_content.value.split('\n\n'):
            print(line)
            if ":" in line:
                sp = line.split(":")
                activities_dic[sp[0]] = sp[1]
            else:
                activities.append(line)
        print(activities)
        print(activities_dic)


    else:
        print(run.status)