import psutil as p

porcentagem = p.cpu_percent(interval=1, percpu=True)
print(porcentagem)