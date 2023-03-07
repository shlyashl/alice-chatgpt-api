**Запуск тестовой среды:** <br>
```start C:\Users\ch\go\bin\alice-nearby.exe --webhook=http://127.0.0.1:5000/api/alice -p 5001```
<br><br>
**Endpoint:** <br>
http://45.87.104.115:8321/api/alice
<br><br>
**Тестовый запрос:** 
```curl --location --request POST 'http://45.87.104.115:8321/api/alice' \
--header 'Content-Type: application/json' \
--data-raw '{
        "request": {"original_utterance": "Привет"},
        "session": {"session_id": "AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA"}, 
        "version": "1.0"
    }'
