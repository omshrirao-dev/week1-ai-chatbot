Day 1 — Done ✓
- Built a working CLI chatbot using Groq API
- Model names can get deprecated — always check provider docs
- System prompt = personality of the AI
- Conversation history = how AI fakes memory
- max_tokens controls response length
- Debugged 3 real errors: 400, 404, KeyboardInterrupt

understanding : 1. always check the available models . 
                2. System Prompth Changes -->  AI Responses Changes


Tomorrow: Day 2 — HTTP requests and FastAPI


127.0.0.1:8000 — localhost, your machine, port 8000. Only you can access it during development.

HTTP methods — GET reads, POST sends data. Every API in the world uses this.

FastAPI — turns Python functions into web endpoints using decorators.

Pydantic — validates data coming in and going out automatically.

uvicorn — the engine that keeps your app running as a server.

Indentation in Python — not style, it is syntax. Wrong indent = broken code.

Error codes — 400 bad request, 404 not found, 200 success. You can now read any API error and know immediately where the problem is.

System design — you can now draw and explain how all the pieces connect. That skill is what engineers use in interviews and client meetings every day.

Day 2 — Done
Built: CLI chatbot converted to FastAPI web API
Learned: HTTP, FastAPI, Pydantic, uvicorn, localhost, ports
Errors fixed: indentation error, uvicorn PATH issue
Understood: full system design — .env → api.py → Groq → response
Confused about: nothing (or write anything still fuzzy)





Tomorrow: Day 3 — error handling + requirements.txt

DAY 3:

What we add today:

1. requirements.txt — so anyone can run your project
2. Proper error handling — so the app never crashes
3. Environment validation — catch missing API key before it crashes
4. Intentionally break it 5 ways — understand every failure mode

With HTTPException — you control exactly what error message the user sees.
Logging prints useful information to the terminal as things happen.

UNDERSTANDING

Server starts → reads .env → loads key into memory
                                      ↓
You change .env → memory unchanged → still works

When you changed the .env file — your server was already running. The server loaded the API key into memory when it first started. That key is sitting in memory as the variable api_key. Changing the .env file after the server started does not affect what is already in memory.
But wait — you have --reload on. Why didn't it reload?

--reload watches for changes to your Python files — .py files. It does NOT watch .env files. So changing .env never triggers a reload.


Break 2 — what Groq returns when key is wrong

     401 = "I know who you are trying to be — but your credentials are wrong."

     403 which means "I know who you are — but you don't have permission."

     httpx. You never imported httpx. You never wrote httpx anywhere. But it appears in your logs. Why?

        Because the Groq SDK uses httpx internally to make HTTP requests. This is a library inside a library. You are seeing the internals of Groq's SDK in your logs. This is what logging reveals — the full chain of what is actually happening under the hood.

    Your server did NOT crash. After that 500 error — your server is still running. Try sending another message right now. It will work fine.

Without your try/except — that 401 from Groq would have crashed the entire server. Every user after that gets nothing until someone restarts it.

With your try/except — one bad request is handled, logged, cleaned up, and the server moves on.



Break 4 — what Pydantic does with wrong data type
     
     Observation : The AI sees "Hi" Command whenever there is empty message input executes

     This is a bug. A real production bug.
     Your app accepts empty messages and wastes an API call on them. In production — this costs money and pollutes your conversation history.

     strip() removes spaces too — so " " (just spaces) also gets rejected.

     Why HTTPException specifically ??
        
        Normal Python errors crash your program with ugly output. HTTPException is FastAPI's way of stopping a request cleanly and sending a proper HTTP response back to the user.

    Why except Exception as e  ?

        Exception is the parent of almost every possible error in Python. Network error, timeout error, key error, type error — they are all children of Exception.

        Writing except Exception means "catch anything that goes wrong — I don't care exactly what type of error it is, I just want to handle it."

        as e stores the actual error in a variable called e so you can read what went wrong and log it.       

OVERALL
    
Day 3 — Done ✓

        Built: error handling + logging + validation + requirements.txt
        Learned: try/except, HTTPException, logging levels,
                fail-fast, rollback, 400 vs 500 status codes
        Broke it 5 ways:
        1. Empty key     → ValueError at startup
        2. Wrong key     → 401 from Groq → 500 to user
        3. Empty message → 400 validation error
        4. Wrong type    → 422 Pydantic auto-catch
        5. Missing .env  → ValueError at startup
        Key insight: validation before try, unexpected failures inside try
        Tomorrow: Day 4 — Git + push to GitHub

Day 4 — Done ✓

        Built: pushed week1-chatbot project to GitHub
        Learned: git init, git add, git commit, git push, git pull
        Fixed: push rejection error — always pull before push
        Key insight: .gitignore protects secrets from going public
                    pull before push when remote has changes
        GitHub: github.com/omshrirao-dev/week1-ai-chatbot
        Tomorrow: Day 5 — conversation memory + system prompt experiments# After every meaningful change
        git add .
        git commit -m "what you changed and why"
        git push






DAY-5 


Day 5 — Done ✓
        Built: system prompt engineering + memory limits + /reset endpoint
        Learned: prompt engineering, sliding window memory,
                Python scope, global keyword
        Built alone: /reset endpoint — first solo feature
        Key insight: AI behavior = system prompt instructions
                    Assign global inside function = need global keyword
                    Every behavior must be explicitly told to AI
        Tomorrow: Day 6 — convert chatbot to streaming responses



CONCEPT OF FILE HANDELING

            What each new concept does:

        os.makedirs(folder, exist_ok=True) — creates the folder. exist_ok=True means if folder already exists — do not crash, just continue.

        os.listdir(folder) — lists all files in the folder. Returns a list of filenames.

        f.startswith("chat_") and f.endswith(".json") — filters only your chat files, excludes index.json.

        str(sequence_number).zfill(3) — converts number to 3-digit string with leading zeros. So 1 becomes "001", 12 becomes "012". This keeps files sorted correctly in the folder.

        os.path.join(folder, filename) — safely combines folder path and filename. Works on Windows AND Mac/Linux without you worrying about / vs \.

        os.path.exists(path) — checks if a file already exists. Returns True or False.

python -m uvicorn api:app --reload        

