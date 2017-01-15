from PythonClientAPI.libs.Game import PointUtils
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.Entities import *
from PythonClientAPI.libs.Game.World import *
import math
import random

class PlayerAI:

    #Class data structures
    prev_goal = [None, None, None, None]
    goal_reached = [False,False,False,False]
    bot_failed_moves = [[],[],[],[]] #List of lists - each list contains a series of tuples that correspond to previous failed move positions
    position_history = [[],[],[],[]]

    def __init__(self):
        pass

    # Returns closest locs for a friendly unit in a list. Each list contains the ordering of tuples that are closest to set of point
    def closest_loc_finder(self, source, items, world, friendly_unit): #Source says where to start from ...

        # Empty List Check
        if (len(items) == 0):
            return []

        #Acquire unit's position and make a distance list
        unit_pos = source

        dist_list = []
        for item in items:
            dist = world.get_path_length(unit_pos, item)  # Get distance between current position and pickup
            dist_list.append(dist)

        # Merge the two lists and sort it (default sort sorts by second elem)
        combined_list = list(zip(items, dist_list))
        #print("Combined list before and after sorting!")
        #print(combined_list)
        combined_list = sorted(combined_list,key = lambda x: x[1])
        #print(combined_list)

        # Return only the pickup-portion of zipped list
        return_list = []
        for elem in combined_list:
            return_list.append(elem[0])

        return return_list

    def do_move(self, world, enemy_units, friendly_units):
        """
        This method will get called every turn; Your glorious AI code goes here.
        
        :param World world: The latest state of the world.
        :param list[EnemyUnit] enemy_units: An array of all 4 units on the enemy team. Their order won't change.
        :param list[FriendlyUnit] friendly_units: An array of all 4 units on your team. Their order won't change.
        """

        ######VERSION INFO########
        #In this version, the bots move to collect powerups and then capture previously unheld control points
        #Optimized!

        #Obtain all power up locations
        pickups_laser_rifle = world.get_positions_of_pickup_type(PickupType.WEAPON_LASER_RIFLE)
        pickups_rail_gun = world.get_positions_of_pickup_type(PickupType.WEAPON_RAIL_GUN)
        pickups_mini_blaster = world.get_positions_of_pickup_type(PickupType.WEAPON_MINI_BLASTER)
        pickups_scatter_gun = world.get_positions_of_pickup_type(PickupType.WEAPON_SCATTER_GUN)
        pickups_shield = world.get_positions_of_pickup_type(PickupType.SHIELD)
        pickups_repair_kit = world.get_positions_of_pickup_type(PickupType.REPAIR_KIT)

        # Aggregate all existing pickups into single list
        pickups = pickups_laser_rifle + pickups_rail_gun + pickups_mini_blaster + pickups_scatter_gun + pickups_shield + pickups_repair_kit

        #Sorted pickups is a list of lists
        sorted_pickups = []
        sorted_pickups_0 = self.closest_loc_finder(friendly_units[0].position,pickups, world, friendly_units[0])
        sorted_pickups.append(sorted_pickups_0)
        sorted_pickups_1 = self.closest_loc_finder(friendly_units[1].position,pickups, world, friendly_units[1])
        sorted_pickups.append(sorted_pickups_1)
        sorted_pickups_2 = self.closest_loc_finder(friendly_units[2].position,pickups, world, friendly_units[2])
        sorted_pickups.append(sorted_pickups_2)
        sorted_pickups_3 = self.closest_loc_finder(friendly_units[3].position,pickups, world, friendly_units[3])
        sorted_pickups.append(sorted_pickups_3)

        #Accumulate all control points
        control_points = world.control_points
        #print("Control Points:",control_points)
        #print("Control points[0].position",control_points[0].position)
        #print("Control points[1].position",control_points[1].position)

        control_point_positions = []
        for control_point in control_points:
            control_point_positions.append(control_point.position)

        #Simple program to obtain all available powerups
        for i in range(0,4): #Runs once per friendly unit

            unit = friendly_units[i]
            unit_pos = unit.position

            prev_move_was_error = False

            print("Unit:", i)
            # print("Position:",unit_pos)

            #Update position list
            if (len(self.position_history[i]) < 3):
                self.position_history[i].append(unit_pos)
            else:
                self.position_history[i].remove(self.position_history[i][0])
                self.position_history[i].append(unit_pos)

            #print(sorted_pickups[i])

            #Iterate through other bots' goals and remove their prev_dest from your sorted_pickups
            removables = list(range(0, 4))
            removables.remove(i)

            for removable in removables:
                if (self.prev_goal[removable] in sorted_pickups[i]):
                    sorted_pickups[i].remove(self.prev_goal[removable])

            #print(sorted_pickups[i])

            #Check status of previous move!
            prev_move_result = unit.last_move_result
            print("Previous Move:",prev_move_result)
            move_success = None

            if (prev_move_result == MoveResult.MOVE_COMPLETED or prev_move_result == MoveResult.NO_MOVE_ATTEMPTED): #None for first round?
                move_success = True
                if (len(self.bot_failed_moves[i]) > 0):
                    self.bot_failed_moves[i] = [] #Reset failed moves sublist for current bot
                    prev_move_was_error = True
                print("MOVE SUCCESS")
            else:
                move_success = False
                if (self.bot_failed_moves[i] == []): #If failed_moves list is empty, add current position to it
                    self.bot_failed_moves[i].append(unit_pos)
                else: #Otherwise, add the previous goal to it
                    self.bot_failed_moves[i].append(self.prev_goal[i])
                print("MOVE FAILURE!!!")

            if(move_success):

                #If list of pickups isn't empty ...
                if (sorted_pickups[i] != []):
                    print("in if")

                    if (self.prev_goal[i] == None):
                        pickup_loc = sorted_pickups[i][0]
                        self.prev_goal[i] = sorted_pickups[i][0]
                        #print("Initialized bot_prev_dest[i]",self.prev_goal[i])
                    elif ((self.goal_reached[i]) and not(prev_move_was_error) and (len(sorted_pickups[i])) > 0):
                        pickup_loc = sorted_pickups[i][0] #sorted_pickups[i] indexes an individual sorted_pickups list!
                        self.prev_goal[i] = sorted_pickups[i][0]
                        self.goal_reached[i] = False
                        #print("Pickup Location Set:", pickup_loc)
                    else:
                        pickup_loc = self.prev_goal[i] #Do not update state/flag since it remains the same
                        #print("Pickup Location Remains the Same!")


                else: #Otherwise, all pickups are currently being tracked, so go get your pickup
                    print("in else")

                    #Get list of closest control points
                    sorted_control_point_positions = self.closest_loc_finder(friendly_units[i].position,control_point_positions, world, friendly_units[i])
                    sorted_control_points = []

                    cp_list_length = len(sorted_control_point_positions)
                    cp_index = 0
                    control_point_found = False
                    pickup_loc = None #Declare it here since you're only assigning values in loops/if statements

                    for_count = 0
                    for cp_position in sorted_control_point_positions:

                        point_found = False

                        point_index = 0

                        while (not(point_found) and point_index < cp_list_length):
                            #print("Control points[point_index] position",control_points[point_index].position,"cp_position",cp_position)
                            if(control_points[point_index].position == cp_position):
                                point_found = True
                                #print("Point found!!!")
                                sorted_control_points.append(control_points[point_index])
                            point_index += 1

                        #print("loop count",for_count,"sorted_control_points length",len(sorted_control_points))
                        for_count += 1


                    #Find the closest control point to move to!
                    while ((cp_index < cp_list_length) and not(control_point_found)):
                        #print("cp_index",cp_index,"sorted_control_points length",len(sorted_control_points))
                        closest_point = sorted_control_points[cp_index]
                        point_pos = closest_point.position
                        point_controlling_team = closest_point.controlling_team
                        print(closest_point)
                        num_enemy_units = closest_point.get_num_enemy_units_around()
                        print("ENEMY UNITS!!!:",num_enemy_units)
                        point_is_main_frame = closest_point.is_mainframe
                        #point_enemies = closest_point.enemies
                        #print("number of enemies:",point_enemies)

                        if (point_controlling_team == friendly_units[i].team):
                            pass #Do nothing if point already controlled
                        elif (point_controlling_team == enemy_units[i].team and num_enemy_units > 0):
                            pass
                        elif (num_enemy_units > 0):
                            pass
                        else:
                            pickup_loc = point_pos
                            control_point_found = True

                        cp_index += 1

                    #If all points have been controlled by your team, move to closest point!
                    if (cp_index == cp_list_length):
                        pickup_loc = sorted_control_points[0].position

                #print(pickup_loc)

            else:
                print("PROCESSING: MOVE WAS A FAILURE!")
                #Obtain current position
                curr_pos = unit.position
                (x,y) = curr_pos
                prev_positions = self.bot_failed_moves[i]

                #Compute neighbouring positions
                adjacent_positions = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]

                print("pos history:",self.position_history[i])
                print("adjacent positions pre:",adjacent_positions)
                if self.position_history[i][1] in adjacent_positions:
                    adjacent_positions.remove(self.position_history[i][1])
                if self.position_history[i][0] in adjacent_positions:
                    adjacent_positions.remove(self.position_history[i][0])
                print("adjacent positions post:",adjacent_positions)

                print("Adjacent Positions (pre):",adjacent_positions)
                print("Prev Positions (pre):",prev_positions)
                for prev_pos in prev_positions:
                    if prev_pos in adjacent_positions:
                        adjacent_positions.remove(prev_pos)
                print("Adjacent Positions (post):",adjacent_positions)

                #Sort paths by closest to destination
                sorted_adjacent_positions = self.closest_loc_finder(self.prev_goal[i],adjacent_positions, world, friendly_units[i])

                #Remove all the zero paths from the list
                print("Sorted adjacent positions:",sorted_adjacent_positions)
                print("Previous failed positions:",prev_positions)
                for sorted_pos in sorted_adjacent_positions:
                    for failed_pos in prev_positions:
                        print("sorted pos:", sorted_pos, "prev_pos", failed_pos)
                        if world.get_path_length(sorted_pos,failed_pos) == 0:
                            sorted_adjacent_positions.remove(sorted_pos)

                #Set the pickup_loc as sorted_adjacent_positions[0]
                #sorted_adj_range = len(sorted_adjacent_positions)
                #rand_pos = random.randint(0,1)
                pickup_loc = sorted_adjacent_positions[0]

            #Statements to decide if you should move/take action
            if (pickup_loc == unit_pos):
                unit.pickup_item_at_position()
                self.goal_reached[i] = True #Set goal flag
            else:
                unit.move_to_destination(pickup_loc)








