from openai import OpenAI
api_key=""
client = OpenAI(api_key=api_key)
thread = client.beta.threads.create()

my_assistant = client.beta.assistants.retrieve("asst_vVnuxiNoKNc2OVzWCOMVOK7o")
print(my_assistant)


message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="화':9:00 ~ 12:00=수업 다른 활동은 어떤걸 하면 좋을까?"
)
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=my_assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)
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


