import random
import csv

def coinToss(target=0, thumb_count=0):
    """
    Description: Similate a coin toss
    Target: The "desired" result
    thumb_count: The number of Krark's Thumbs in play

    """
    results = []
    tosses = 2**thumb_count
    for i in range(0,tosses):
        flip = random.randint(0, 1)
        results.append(flip)
        if flip == target:
            # This is to save time
            # If we get at least one "correct" result we can stop
            break
    return flip

runs = 1000
output_file = "results.csv"
additional_krark_triggers = 1

with open(output_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Run", "Iterations", "Mana", "Magecraft"])
    for run in range(1, runs + 1):
        mana = 3 # Seething song costs three mana, lets assume we start on three
        seething_song_in_hand = True
        iteration = 0
        magecraft = 0

        # Krarkashima loops continue for as long as Seething Song returns to our hand, and we have three mana to cast it
        # iteration limit to stop it running unbound
        while seething_song_in_hand and mana >= 3 and iteration < 100:
            iteration += 1
            magecraft += 1
            mana -= 3 # spending mana to cast song
            seething_song_inhand = False # song on the stack, not in hand
            krark_trigger = coinToss()
            # We "lose" the flip and return song to hand
            if krark_trigger == 0: 
                seething_song_in_hand = True
            # Copy song and gain 5 mana
            else:
                magecraft += 1
                mana += 5

            heads_and_tails_achieved = False
            for i in range(0, additional_krark_triggers):
                # Repeat for additional krark triggers
                # We want one of each result to loop the spell
                # f(x) = 1 - x, f(0) = 1, f(1) = 0
                if heads_and_tails_achieved == False:
                    # Objective 1: Get one heads and one tails for Krark triggers
                    target = 1 - krark_trigger
                else:
                    # Objective 2: Once heads and tails is achieved copy the spell as much as possible
                    target = 1
                additional_trigger = coinToss(target)
                if additional_trigger == 0: 
                    seething_song_in_hand = True
                else:
                    magecraft += 1
                    mana += 5

            if seething_song_in_hand == False:
                # this represents all krark triggers copying the spell
                # seething song goes from the stack to the grave, and does not get returned to hand
                # the original spell then resolves adding five mana
                # this is the only scenario where the original spell can resolve
                mana += 5

        writer.writerow([run, iteration, mana, magecraft])

