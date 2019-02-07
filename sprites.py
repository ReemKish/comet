def construct(namespace, index_list):
    for i, n in enumerate(index_list):
        index_list[i] = str(n).zfill(2)
    return ['textures\\sprites\\{0}\\{0}_{1}.png'.format(namespace, i) for i in index_list]


# ------------------------------------------------------ Sprites -------------------------------------------------------
spaceship1 = construct('spaceship1', list(range(10)))
spaceship2 = construct('spaceship2', list(range(10)))
missile2 = construct('missile2', [0,1,2])
missile1 = construct('missile1', [0,1,2])
bg = construct('background', [0])
