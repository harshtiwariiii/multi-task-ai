import os
print("Environment variables:", [k for k in os.environ if "OPENAI" in k])