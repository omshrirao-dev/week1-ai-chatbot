═══════════════════════════════════════════════════════
WEEK 1 ERROR LOG — add to LEARNING.md
═══════════════════════════════════════════════════════

ERROR 1 — Model decommissioned
──────────────────────────────
Error:    groq.BadRequestError: 400 — model `llama3-8b-8192` 
          has been decommissioned
When:     Day 1 — first time running chatbot.py
Why:      Groq retired the old model. Model names expire 
          when AI providers release newer versions.
Fix:      Changed model name to a current one.
          Used client.models.list() to see available models.
Lesson:   Always verify model names from official provider 
          docs before hardcoding. Model names go stale.

───────────────────────────────────────────────────────

ERROR 2 — Model not found
──────────────────────────────
Error:    groq.NotFoundError: 404 — model does not exist 
          or you do not have access
When:     Day 1 — trying different model names
Why:      Some models exist but are not available on free 
          tier accounts. 404 = found the server but not 
          that specific resource.
Fix:      Listed all available models with client.models.list()
          Picked one from the actual list.
Lesson:   404 = resource not found. Always verify from 
          your own account, not documentation alone.

───────────────────────────────────────────────────────

ERROR 3 — API key not loading
──────────────────────────────
Error:    Key found: NOT FOUND (or None)
When:     Day 1 — debugging why model calls failed
Why:      .env file was in wrong folder OR load_dotenv() 
          was not called before os.environ.get()
Fix:      Added debug print to check if key was loading.
          Confirmed .env file location matches chatbot.py.
Lesson:   .env file must be in SAME folder as your Python 
          file. load_dotenv() must run BEFORE any 
          os.environ.get() call. Order matters.

───────────────────────────────────────────────────────

ERROR 4 — KeyboardInterrupt
──────────────────────────────
Error:    KeyboardInterrupt
When:     Day 1 — pressing Ctrl+C to stop the program
Why:      Not actually an error. Ctrl+C sends an interrupt 
          signal to stop any running program.
Fix:      Nothing to fix. This is intentional.
Lesson:   Ctrl+C = stop any running program in terminal.
          KeyboardInterrupt is not a bug — it is a signal.

───────────────────────────────────────────────────────

ERROR 5 — Red underline on load_dotenv
──────────────────────────────
Error:    Expected indented block — Pylance red underline
When:     Day 1 — writing chatbot.py in VS Code
Why:      python-dotenv library was not installed. 
          VS Code could not find the module.
Fix:      pip install python-dotenv
Lesson:   Red underline in VS Code = either syntax error 
          OR missing library. Check both before panicking.

───────────────────────────────────────────────────────

ERROR 6 — uvicorn not recognized
──────────────────────────────
Error:    FullyQualifiedErrorId: CommandNotFoundException
When:     Day 2 — trying to run uvicorn api:app --reload
Why:      uvicorn installed but Windows PATH did not 
          register it as a global command.
Fix:      python -m uvicorn api:app --reload
          Using python -m bypasses PATH issues entirely.
Lesson:   When a command is not found — try python -m 
          before the command name. Works for uvicorn, 
          pytest, pip, and most Python tools.

───────────────────────────────────────────────────────

ERROR 7 — Indentation error
──────────────────────────────
Error:    Expected indented block — Pylance red underline
          Function body appeared empty
When:     Day 2 — writing api.py chat() function
Why:      Code inside def chat() was not indented. 
          Python uses indentation as syntax — not just style.
          Also had uvicorn command written inside .py file.
Fix:      Indented all code inside the function by 4 spaces.
          Removed uvicorn command from Python file — 
          it is a terminal command not Python code.
Lesson:   Python indentation IS syntax. Wrong indent = 
          broken code. Terminal commands never go inside 
          .py files.

───────────────────────────────────────────────────────

ERROR 8 — 401 Unauthorized from Groq
──────────────────────────────
Error:    groq.AuthenticationError: 401 — Invalid API Key
When:     Day 3 — Break 2, testing wrong API key
Why:      Groq received the request but rejected the key.
          401 = authentication failed. Server knows you 
          are trying to authenticate but credentials wrong.
Fix:      Put correct API key back in .env file.
          Restart server after changing .env.
Lesson:   401 = wrong credentials.
          403 = right credentials, wrong permissions.
          Always restart server after changing .env —
          environment variables load ONCE at startup.

───────────────────────────────────────────────────────

ERROR 9 — Empty message returning AI response
──────────────────────────────
Error:    Sending empty string still got AI response
When:     Day 3 — Break 3, testing empty message
Why:      Pydantic only validates DATA TYPE — is it a string?
          Empty string "" IS a valid string. Type check passed.
          Business logic validation is YOUR job to write.
Fix:      Added manual check before try block:
          if not request.message.strip():
              raise HTTPException(400, "Message cannot be empty")
Lesson:   Pydantic = type validation (automatic)
          Business rules = your validation (manual)
          Never rely on Pydantic for business logic.

───────────────────────────────────────────────────────

ERROR 10 — Validation returning 500 instead of 400
──────────────────────────────
Error:    Empty message check returning 500 not 400
When:     Day 3 — fixing Break 3
Why:      HTTPException was raised INSIDE try block.
          except Exception caught it and overrode it 
          with a 500 error. Your own intentional error 
          got swallowed by the catch-all.
Fix:      Moved validation BEFORE the try block.
Lesson:   GOLDEN RULE — never forget this:
          Before try  = YOUR intentional validations (400)
          Inside try  = unexpected external failures (500)
          except      = catches only unexpected failures
          These must never be mixed.

───────────────────────────────────────────────────────

ERROR 11 — Server not restarting after .env change
──────────────────────────────
Error:    Changed .env but server still worked normally
When:     Day 3 — Break 1, testing empty API key
Why:      --reload watches .py files only, not .env files.
          Environment variables load into memory at startup.
          Changing the file does not change what is in memory.
Fix:      Always Ctrl+C and restart server after .env changes.
Lesson:   Environment variables = loaded ONCE at startup.
          Change .env = must restart server.
          This is true everywhere — local, Render, Railway, AWS.

───────────────────────────────────────────────────────

ERROR 12 — Missing .env file
──────────────────────────────
Error:    ValueError: GROQ_API_KEY not found in .env file
When:     Day 3 — Break 5, renaming .env to .env.backup
Why:      .env file did not exist so load_dotenv() found 
          nothing. api_key variable was None. 
          Fail-fast validation caught it immediately.
Fix:      Rename .env.backup back to .env. Restart server.
Lesson:   Fail-fast = catch problems at startup not runtime.
          Server crashing at startup with clear message 
          is BETTER than crashing mid-request with 
          confusing error. Always validate critical 
          config at startup.

═══════════════════════════════════════════════════════
STATUS CODES LEARNED THIS WEEK
═══════════════════════════════════════════════════════

200 → Success. Everything worked.
400 → Bad Request. YOUR input was wrong.
401 → Unauthorized. Wrong credentials/API key.
403 → Forbidden. Right credentials, wrong permissions.
404 → Not Found. Resource does not exist.
422 → Unprocessable. Pydantic validation failed.
500 → Internal Server Error. Server side problem.

═══════════════════════════════════════════════════════
KEY CONCEPTS LEARNED THIS WEEK
═══════════════════════════════════════════════════════

Fail-fast        → crash loudly at startup, not silently later
Rollback         → undo changes when something fails
Try/except       → safety net for unexpected failures
HTTPException    → controlled emergency exit for requests
Logging          → making your system visible and debuggable
Requirements.txt → makes project portable to any machine
Localhost        → 127.0.0.1, your machine only, not internet
Port             → door number, 8000 is yours
Restart rule     → always restart after .env changes

═══════════════════════════════════════════════════════