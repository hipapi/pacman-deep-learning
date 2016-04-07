# featureExtractors.py
# --------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"Feature extractors for Pacman game states"

from game import Directions, Actions
import util

class FeatureExtractor:  
  def getFeatures(self, state, action):    
    """
      Returns a dict from features to counts
      Usually, the count will just be 1.0 for
      indicator functions.  
    """
    util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
  def getFeatures(self, state, action):
    feats = util.Counter()
    feats[(state,action)] = 1.0
    return feats

def closestFood(pos, food, walls):
  """
  closestFood -- this is similar to the function that we have
  worked on in the search project; here its all in one place
  """
  fringe = [(pos[0], pos[1], 0)]
  expanded = set()
  while fringe:
    pos_x, pos_y, dist = fringe.pop(0)
    if (pos_x, pos_y) in expanded:
      continue
    expanded.add((pos_x, pos_y))
    # if we find a food at this location then exit

    if food[pos_x][pos_y]:
      return dist
    # otherwise spread out from the location to its neighbours
    nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
    for nbr_x, nbr_y in nbrs:
      fringe.append((nbr_x, nbr_y, dist+1))
  # no food found
  return None

def closestScaredGhost(pos, scaredGhostsOne, walls):

  fringe = [(pos[0], pos[1], 0)]
  expanded = set()
  while fringe:
    pos_x, pos_y, dist = fringe.pop(0)
    if (pos_x, pos_y) in expanded:
      continue
    expanded.add((pos_x, pos_y))
    # if we find a food at this location then exit

    if scaredGhostsOne == (pos_x,pos_y):
      return dist
    if scaredGhostsOne == (pos_x - .5,pos_y - 0.5):
      return dist
    if scaredGhostsOne == (pos_x + .5,pos_y + 0.5):
      return dist
    if scaredGhostsOne == (pos_x + .5,pos_y):
      return dist
    if scaredGhostsOne == (pos_x ,pos_y + 0.5):
      return dist
    if scaredGhostsOne == (pos_x ,pos_y - 0.5):
      return dist
    if scaredGhostsOne == (pos_x - .5,pos_y ):
      return dist
    # otherwise spread out from the location to its neighbours
    nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
    for nbr_x, nbr_y in nbrs:
      fringe.append((nbr_x, nbr_y, dist+1))
  # no food found
  return None

class SimpleExtractor(FeatureExtractor):
  """
  Returns simple features for a basic reflex Pacman:
  - whether food will be eaten
  - how far away the next food is
  - whether a ghost collision is imminent
  - whether a ghost is one step away
  """
  
  def getFeatures(self, state, action):
    # extract the grid of food and wall locations and get the ghost locations
    food = state.getFood()
    walls = state.getWalls()
    ghosts = state.getGhostPositions()

    features = util.Counter()
    
    features["bias"] = 1.0
    
    # compute the location of pacman after he takes the action
    x, y = state.getPacmanPosition()
    dx, dy = Actions.directionToVector(action)
    next_x, next_y = int(x + dx), int(y + dy)
    
    # count the number of ghosts 1-step away
    features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

    # if there is no danger of ghosts then add the food feature
    if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
      features["eats-food"] = 1.0
    
    dist = closestFood((next_x, next_y), food, walls)
    if dist is not None:
      # make the distance a number less than one otherwise the update
      # will diverge wildly
      features["closest-food"] = float(dist) / (walls.width * walls.height) 
    features.divideAll(10.0)
    return features

# class setnumberExtractor(FeatureExtractor):
#   """
#   Returns simple features for a basic reflex Pacman:
#   - whether food will be eaten
#   - how far away the next food is
#   - whether a ghost collision is imminent
#   - whether a ghost is one step away
#   """
#
#   def getFeatures(self, state, action):
#     # extract the grid of food and wall locations and get the ghost locations
#     # food = state.getFood()
#     # walls = state.getWalls()
#     # ghost = state.getGhostState()
#     # ghosts = state.getGhostPositions()
#     # scaredGhostsOne = state.getGhostState(1)
#     # scaredGhostsTwo = state.getGhostState(2)
#     # scaredGhostsOne.scaredTimer = state.getScaredGhostTimer(1)
#     # scaredGhostsTwo.scaredTimer = state.getScaredGhostTimer(2)
#     # features = util.Counter()
#     # print ghost
#     #
#     # features["#-of-ghosts-1-step-away"] = 0
#     # features["eats-food"] = 0
#     # features["closest-food"] = 0
#     # features["scared-ghosts"] = 0
#     #
#     # # compute the location of pacman after he takes the action
#     # x, y = state.getPacmanPosition()
#     # dx, dy = Actions.directionToVector(action)
#     # next_x, next_y = int(x + dx), int(y + dy)
#     #
#     # # count the number of ghosts 1-step away
#     # features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)
#     #
#     # # if there is no danger of ghosts then add the food feature
#     # # if scaredGhostsOne.scaredTimer >= 1:
#     # #   eatGhostsOne = True
#     # # else:
#     # #   eatGhostsOne = False
#     # # if scaredGhostsTwo.scaredTimer >= 1:
#     # #   eatGhostsTwo = True
#     # # else:
#     # #   eatGhostsTwo = False
#     # # if eatGhostsOne and eatGhostsTwo:
#     # #
#     # #   ghost1 = state.getGhostPosition(1)
#     # #
#     # #   ghost2 = state.getGhostPosition(2)
#     # #
#     # #   dist1 = closestScaredGhost((next_x, next_y), ghost1, walls,food)
#     # #   dist2 = closestScaredGhost((next_x, next_y), ghost2, walls,food)
#     # #   if dist1 > dist2:
#     # #     features["scared-ghosts"] = float(dist1) / (walls.width * walls.height)
#     # #   elif dist2 > dist1:
#     # #     features["scared-ghosts"] = float(dist2) / (walls.width * walls.height)
#     # #   features["eats-food"] = 1.0
#     # #   features["closest-food"] = 1.0
#     # # elif eatGhostsOne:
#     # #
#     # #   features["scared-ghosts"] = 1.0
#     # #   features["eats-food"] = 1.0
#     # #   features["closest-food"] = 1.0
#     # # elif eatGhostsTwo:
#     # #   features["scared-ghosts"] = 1.0
#     # #   features["eats-food"] = 1.0
#     # #   features["closest-food"] = 1.0
#     # # else:
#     # if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
#     #  features["eats-food"] = 1.0
#     #  dist = closestFood((next_x, next_y), food, walls)
#     #  if dist is not None:
#     #    features["closest-food"] = float(dist) / (walls.width * walls.height)
#     food = state.getFood()
#     walls = state.getWalls()
#     ghosts = state.getGhostPositions()
#
#     features = util.Counter()
#
#     features["#-of-ghosts-1-step-away"] = 0
#     features["eats-food"] = 0
#     features["closest-food"] = 0
#
#
#     # compute the location of pacman after he takes the action
#     x, y = state.getPacmanPosition()
#     dx, dy = Actions.directionToVector(action)
#     next_x, next_y = int(x + dx), int(y + dy)
#
#     # count the number of ghosts 1-step away
#     features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)
#
#     # if there is no danger of ghosts then add the food feature
#     if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
#       features["eats-food"] = 1.0
#
#     dist = closestFood((next_x, next_y), food, walls)
#     if dist is not None:
#       # make the distance a number less than one otherwise the update
#       # will diverge wildly
#       features["closest-food"] = float(dist) / (walls.width * walls.height)
#     features.divideAll(10.0)
#     return features
#
#
#
#
#     features.divideAll(10.0)
#     return features
class setnumberExtractor(FeatureExtractor):
  """
  Returns simple features for a basic reflex Pacman:
  - whether food will be eaten
  - how far away the next food is
  - whether a ghost collision is imminent
  - whether a ghost is one step away
  """

  def getFeatures(self, state, action):
    # extract the grid of food and wall locations and get the ghost locations
    food = state.getFood()
    walls = state.getWalls()
    ghosts = state.getGhostPositions()
    pacman = state.getPacmanPosition()
    scaredGhostsOne = state.getGhostState(1)
    scaredGhostsTwo = state.getGhostState(2)
    scaredGhostsOne.scaredTimer = state.getScaredGhostTimer(1)
    scaredGhostsTwo.scaredTimer = state.getScaredGhostTimer(2)
    features = util.Counter()
# #     # print ghost
#     features = util.Counter()

    features["#-of-ghosts-1-step-away"] = 0
    features["eats-food"] = 0
    features["closest-food"] = 0
    features['closest-scared-ghost'] = 0
    features['pacman-y'] = 0
    features['pacman-x'] = 0
    features['ghost1-x'] = 0
    features['ghost1-y'] = 0
    features['ghost2-x'] = 0
    features['ghost2-y'] = 0
    ghost1 = state.getGhostPosition(1)
    ghost2 = state.getGhostPosition(2)
    firstitem = 1;
    for x in ghost1:
      if firstitem==1:
       features['ghost1-x'] = x
       firstitem+=1
      else:
        features['ghost1-y'] = x
        firstitem = 1
    for x in ghost2:
      if firstitem==1:
       features['ghost2-x'] = x
       firstitem+=1
      else:
        features['ghost2-y'] = x
        firstitem=1
    for x in pacman:
      if firstitem==1:
       features['pacman-x'] = x
       firstitem +=1
      else:
        features['pacman-y'] = x
        firstitem=1
    # features['scared-ghost-one'] = 0
    # features['scared-ghost-two'] = 0

    # compute the location of pacman after he takes the action
    x, y = state.getPacmanPosition()
    dx, dy = Actions.directionToVector(action)
    next_x, next_y = int(x + dx), int(y + dy)

    # count the number of ghosts 1-step away
    NoScaredGhosts = False
    if scaredGhostsOne.scaredTimer >= 1 and scaredGhostsTwo.scaredTimer >=1:
      features["#-of-ghosts-1-step-away"] = 0
    else:
      features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)
    if scaredGhostsOne.scaredTimer >= 1 and scaredGhostsTwo.scaredTimer >=1:


      dist1 = closestScaredGhost((next_x, next_y), ghost1, walls)
      dist2 = closestScaredGhost((next_x, next_y), ghost2, walls)
      if dist1 >= dist2:
        dist = dist2
      elif dist1 <= dist2:
        dist = dist1
      if dist is not None:
      # make the distance a number less than one otherwise the update
      # will diverge wildly
        features['closest-scared-ghost'] = float(dist) / (walls.width * walls.height)
        #features['eats-food'] = 0.01
    # elif scaredGhostsOne.scaredTimer >= 1 and not scaredGhostsTwo.scaredTimer >=1:
    #   ghost1 = state.getGhostPosition(1)
    #   dist1 = closestScaredGhost((next_x, next_y), ghost1, walls)
    #   if dist1 is not None:
    #   # make the distance a number less than one otherwise the update
    #   # will diverge wildly
    #     features['closest-scared-ghost'] = float(dist1) / (walls.width * walls.height)
    # elif not scaredGhostsOne.scaredTimer >= 1 and scaredGhostsTwo.scaredTimer >=1:
    #   ghost2 = state.getGhostPosition(2)
    #   dist2 = closestScaredGhost((next_x, next_y), ghost2, walls)
    #   if dist2 is not None:
    #   # make the distance a number less than one otherwise the update
    #   # will diverge wildly
    #     features['closest-scared-ghost'] = float(dist2) / (walls.width * walls.height)
    else:
      NoScaredGhosts = True

    # if there is no danger of ghosts then add the food feature

    if scaredGhostsOne.scaredTimer >= 1 and state.getGhostPosition(1) == (next_x,next_y):
      features["closest-food"] = 1
    if scaredGhostsTwo.scaredTimer >= 1 and state.getGhostPosition(2) == (next_x,next_y):
      features["closest-food"] = 1
    if NoScaredGhosts:
      if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
        features["eats-food"] = 1.0
      dist = closestFood((next_x, next_y), food, walls)
      if dist is not None:
        # make the distance a number less than one otherwise the update
        # will diverge wildly
        features["closest-food"] = float(dist) / (walls.width * walls.height)
    features.divideAll(10.0)
    print features
    return features
