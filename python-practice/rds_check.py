storage_used_percent = 92
if storage_used_percent > 90:
    print("Critical! Expand your storage immediately.")
elif storage_used_percent >70:
    print("Warning! Storage filling up.")
else:    print("Storage usage is within normal limits.")