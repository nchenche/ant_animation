#!/usr/bin/env python3

import random
import ant_animate


#-----------param start-----------
nbTours = 25
nbFourmis = 10
nbfood = 50
maxcoord = 20
mincoord = 1
pv = 20
penalty = 2
#----------------------------------

#----------functions---------------

def setFood(mini, maxi, nbcouples):

    x = []
    y = []
    for i in range(mini,(maxi+1)) :
        for j in range(mini, (maxi+1)) :
            x.append(i)
            y.append(j)

    couple_indexes = random.sample(range(maxi*maxi), nbcouples)

    foodx =  [x[ci] for ci in couple_indexes]
    foody =  [y[ci] for ci in couple_indexes]

    return foodx, foody


def setFourmis(mini, maxi, nbfourmis, pv):

    d_f = {}
    for fi in range(nbfourmis) :
            
        # init fourmis i
        d_f[fi] = {"x":[], "y":[], "pv":[]}
        d_f[fi]["x"].append(random.randint(mini, maxi))
        d_f[fi]["y"].append(random.randint(mini, maxi))
        d_f[fi]["pv"].append(pv)

    return d_f
        

def move(d_f, ti, fi, mincoord, maxcoord) :

    d_f[fi]["pv"].append(d_f[fi]["pv"][ti-1] - penalty)
    direction = random.choice(["N","S","E","W"])

    if direction == "N" :
        d_f[fi]["x"].append(d_f[fi]["x"][ti-1])
        d_f[fi]["y"].append(d_f[fi]["y"][ti-1] + 1) 

    elif direction == "S" :
        d_f[fi]["x"].append(d_f[fi]["x"][ti-1])
        d_f[fi]["y"].append(d_f[fi]["y"][ti-1] - 1) 

    elif direction == "E" :
        d_f[fi]["x"].append(d_f[fi]["x"][ti-1] + 1)
        d_f[fi]["y"].append(d_f[fi]["y"][ti-1])

    else :
        d_f[fi]["x"].append(d_f[fi]["x"][ti-1] - 1)
        d_f[fi]["y"].append(d_f[fi]["y"][ti-1])


    if d_f[fi]["x"][ti] >= maxcoord :
        d_f[fi]["x"][ti] = d_f[fi]["x"][ti] - 2
        
    elif d_f[fi]["x"][ti] <= mincoord :
        d_f[fi]["x"][ti] = d_f[fi]["x"][ti] + 2

    elif d_f[fi]["y"][ti] >= maxcoord :
        d_f[fi]["y"][ti] = d_f[fi]["y"][ti] - 2

    elif d_f[fi]["y"][ti] <= mincoord :
        d_f[fi]["y"][ti] = d_f[fi]["y"][ti] + 2


    

#set food positions
foodx, foody = setFood(mincoord, maxcoord, nbfood)

# init fourmis with coords (x,y) and pv in a dico
d_f = setFourmis(mincoord, maxcoord, nbFourmis, pv)


# print(d_f)


# loop on each fi for nbTours
# range(1, nbTours) will iterate nbTours - 1 time + the first ite of the init = total of nbTours
for ti in range(1, nbTours) :

    print("Time #", ti)
    for fi in range(nbFourmis):

        if d_f[fi]["pv"][ti-1] >= pv/2 : #moves!

            #print("----pv ok, ", ti, fi, d_f[fi]["pv"], d_f[fi]["x"][ti-1], d_f[fi]["y"][ti-1])
            move(d_f, ti, fi, mincoord, maxcoord)
            #print("after move, ", d_f[fi]["pv"], d_f[fi]["x"][ti], d_f[fi]["y"][ti])

        elif d_f[fi]["pv"][ti-1] < pv/2 and d_f[fi]["pv"][ti-1]  > 0 : # may move and alive!

            moveornot = random.randint(0,1)

            if moveornot == 1 : # moves!
                move(d_f, ti, fi, mincoord, maxcoord)
                
            else : # doesn't move
                d_f[fi]["x"].append(d_f[fi]["x"][ti-1])
                d_f[fi]["y"].append(d_f[fi]["y"][ti-1])
                d_f[fi]["pv"].append(d_f[fi]["pv"][ti-1] - penalty/2)
                
        else: # dead 
                d_f[fi]["x"].append(d_f[fi]["x"][ti-1])
                d_f[fi]["y"].append(d_f[fi]["y"][ti-1])
                d_f[fi]["pv"].append(0)
            

                
        # if finds food, then pv = pvmax
        for foodindex in range(nbfood) :

            if d_f[fi]["x"][ti] == foodx[foodindex] and d_f[fi]["y"][ti] == foody[foodindex]:
                d_f[fi]["pv"][-1] = pv



print('foodx', foodx)
print('foody', foody)

print('fourmis:', d_f)

visual_app = ant_animate.Visual_App(ants_dict=d_f, foodx=foodx, foody=foody, pv=pv, delay=1000)
visual_app.run()
                
        
