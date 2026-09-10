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

═══════════════════════════════════════════════════════
DAY 4 ERROR LOG
═══════════════════════════════════════════════════════

ERROR 1 — Push rejected
──────────────────────────────
Error:    ! [rejected] main -> main (fetch first)
          Updates were rejected because the remote 
          contains work that you do not have locally
When:     Day 4 — first time pushing to GitHub
Why:      You made changes directly on GitHub website
          (adding topics). Now GitHub had newer code
          than your laptop. Git refused to overwrite it.
How YOU handled it:
          You read the error message fully.
          You understood "remote has changes I don't have."
          You ran git pull origin main to sync first.
          Then pushed successfully.
Lesson:   Always pull before push when remote has changes.
          git pull → git push. Never skip pull.

═══════════════════════════════════════════════════════
DAY 5 ERRORS
═══════════════════════════════════════════════════════

ERROR 2 — System prompt syntax mess
──────────────────────────────
Error:    Red underlines everywhere in VS Code
When:     Day 5 — writing custom system prompt
Why:      You wrote system_prompt = "system_prompt = '..."
          Double assignment. Mixed single and double quotes.
          Multi-line string inside single quotes — impossible.
How YOU handled it:
          You spotted something was wrong immediately.
          You pasted the code here and asked for help.
          You learned triple quotes """ for multi-line strings.
Lesson:   Multi-line strings always use triple quotes.
          Never nest quotes of same type inside each other.

───────────────────────────────────────────────────────

ERROR 3 — Scope error on conversation history
──────────────────────────────
Error:    cannot access local variable 'conversation_history'
          where it is not associated with a value
When:     Day 5 — adding memory limit sliding window
Why:      You assigned to conversation_history inside 
          the function. Python treated it as a local 
          variable. But it did not exist locally yet.
          Crash when trying to read it before assigning.
How YOU handled it:
          You read the error — "cannot access local variable"
          You understood it was a scope problem.
          You added global conversation_history at the
          top of the function.
          Tested — memory limit worked perfectly.
Lesson:   Read global variable = no keyword needed.
          Assign global variable inside function = 
          must declare global first. Always.

───────────────────────────────────────────────────────

ERROR 4 — /reset endpoint syntax errors
──────────────────────────────
Error:    IndentationError + invalid syntax
When:     Day 5 — building /reset endpoint alone
Why:      Multiple issues:
          - conversation_history inside decorator
          - print = {...} instead of return
          - Mixed indentation (4 spaces vs 6 spaces)
          - Empty lines between decorator and function
          - comment inside function breaking indentation
How YOU handled it:
          THIS IS THE IMPORTANT ONE.
          You built this completely alone.
          Every attempt got closer to correct.
          Attempt 1: wrong syntax inside decorator
          Attempt 2: wrong assignment to print
          Attempt 3: missing global keyword
          Attempt 4: global keyword present but 
                     indentation wrong
          Attempt 5: comment breaking indentation
          Attempt 6: typed it fresh — WORKED.
          You never gave up. You kept trying.
          You fixed it without me writing it for you.
Lesson:   Decorator and function must have no empty
          line between them.
          Indentation must be consistent — 4 spaces.
          When messy — delete and retype fresh.

───────────────────────────────────────────────────────

ERROR 5 — Reset deletes history permanently
──────────────────────────────
Error:    Not a crash — a product thinking gap
When:     Day 5 — after /reset was working
Why:      Reset cleared history with no backup.
          Data lost forever on every reset.
How YOU handled it:
          THIS IS THE MOST IMPRESSIVE ONE.
          You caught this yourself. I did not point it out.
          You said "we should store history before deleting"
          That is product thinking + engineering thinking
          combined. You thought beyond just making it work.
          You thought about what a real product needs.
Fix:      Adding JSON file storage before clearing.
Lesson:   Working code is not always complete code.
          Always ask "what happens to the data?"
          That question separates engineers from coders.

═══════════════════════════════════════════════════════
SPECIAL MENTION — WHAT YOU DID DIFFERENTLY
═══════════════════════════════════════════════════════

Day 4: You read the git rejection error fully and 
       understood what it meant before asking.
       Most beginners panic. You diagnosed.

Day 5: You built /reset endpoint through 6 attempts
       without giving up once. Each attempt was 
       closer than the last. That persistence is 
       the most important engineering skill.

Day 5: You caught the data loss bug yourself.
       Nobody pointed it out. Your product instinct
       fired naturally. That instinct grows with 
       every project you build.

═══════════════════════════════════════════════════════
RUNNING TOTAL — WEEK 1
═══════════════════════════════════════════════════════

Day 1: 4 errors
Day 2: 2 errors  
Day 3: 5 errors
Day 4: 1 error
Day 5: 4 errors (1 caught by you independently)

Total: 16 errors — 16 lessons — 0 gives up

═══════════════════════════════════════════════════════