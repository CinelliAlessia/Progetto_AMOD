#
ACTION_RANDOM = True
ACTION_CW = True
ACTION_SWEEP = True
ACTION_MIP = False

ACTION_PARSE = ACTION_RANDOM | ACTION_CW | ACTION_SWEEP | ACTION_MIP
print("Working on GitHub ACTION: ", ACTION_PARSE)

#
TIMEOUT_ON = True
if TIMEOUT_ON:
    TIMEOUT = 5*60  # Timeout di 5 minuti (300 secondi)
else:
    TIMEOUT = 86400  # Timeout di 24 ore

