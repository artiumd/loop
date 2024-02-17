import time

from src.loop import loop_over

n = 1_000_000

for x in loop_over(range(n)).returning(enumerations=True, inputs=True, outputs=False).show_progress(total=n, postfix_str=str):
    time.sleep(0.0)
