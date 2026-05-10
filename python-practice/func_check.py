def check_cpu(cpu):
    if cpu > 80:
        return "CRITICAL"
    elif cpu > 50:
        return "WARNING"
    else:
        return "OK"
result = check_cpu(85)
print(result)