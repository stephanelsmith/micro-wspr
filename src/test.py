
from afsk.func import *
# afsk = create_afsk(ampli = 256)
# for i in range(10):
    # print(afsk(0))

tonegen = create_afsk_tone_gen(ampli = 256)
for x in range(10):
    for i in tonegen(x%2):
        print(i)
