# MonaLisa - Image recreation using genetic algorithms

## Introduction

This project is a simple implementation of a genetic algorithm to recreate an image using polygons.

> For more information about genetic algorithms, see [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm).

## First Version
This version is based on this [paper](https://medium.com/@sebastian.y.charmot/genetic-algorithm-for-image-recreation-4ca546454aaa) by Sebastian Charmot.

The first version of the algorithme is based on the following steps:
1. Generate a random population of polygons
2. Compute the fitness of each individual
3. Select the best individual
4. Apply crossover between the best individual and the population (with stocking the previous best individual)
5. Apply mutation to the population (except the previous best individual), which consists in adding a random polygon to all individuals
6. Repeat from step 2, x times to upgrade the image

The result of this different steps are shown below.
| image | 485 generations | 1000 generations |
| --- | --- | --- |
| <img src="img/mona-lisa/mona.png" width="200"/> | <img src="img/mona-lisa/generation485.png" width="200"/> | <img src="img/mona-lisa/mona-lisa-1220.png" width="200"/> |

| image | 500 generations |
| --- | --- |
| <img src="img/nuit-etoilee/nuit-etoilee.png" width="300"/> | <img src="img/nuit-etoilee/nuit-etoilee-500.png" width="300"/>

But After the 1000th generation, the algorithm has a low probability to improve the image anymore, due to the size of the polygons. The algorithm is stuck in a local minimum.

## Second Version

The main problem of the first version is the precision of the polygons. As the polygons are represented by a list of points, the more points are far from others, less the polygon is precies. To solve this problem, I decide to search on progressively reduce the size of the polygons. So the algorithm is based on the following steps:
1. Generate a random population of polygons
2. Compute the fitness of each individual
3. Select the best individual
4. Equilibrate the limit size of the polygons, when the process is stuck (the fitness is not increasing), we will reduce the limit size of the polygons and when the process is not stuck, we will increase the limit size of the polygons.
5. Apply crossover between the best individual and the population (with stocking the previous best individuals)
6. Apply mutation to the population (except the previous best individuals), which consists in adding a random polygon to all individuals
7. Repeat from step 2, x times to upgrade the image

| image | 200 generations | 1000 generations | 2000 generations | 3000 generations | 4000 generations | 5000 generations |
| --- | --- | --- | --- | --- | --- | --- |
| <img src="img/logo/logo.png"/> | <img src="img/logo/res2-200.png" width="200"/> | <img src="img/logo/res2-1000.png" width="200"/> |<img src="img/logo/res2-2000.png" width="200"/> | <img src="img/logo/res2-3000.png" width="200"/> | <img src="img/logo/res2-4000.png" width="200"/> | <img src="img/logo/res2-5000.png" width="200"/> |

In comparison with the first version:
| First version | Second version |
| --- | --- |
| <img src="img/logo/logo-1000.png" width="200"/> | <img src="img/logo/res2-1000.png" width="200"/> |

And for the result on 5000 generations:
| Objectif | Result |
| --- | --- |
| <img src="img/logo/logo.png" width="200"/> | <img src="img/logo/res2-5000.png" width="200"/> |

With this version, the algorithm is able to improve the image without being stuck. Now, the algorithm is able to recreate the image with a precision of 1 pixel.
