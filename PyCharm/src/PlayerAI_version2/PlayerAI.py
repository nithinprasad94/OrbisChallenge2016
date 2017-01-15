from PythonClientAPI.libs.Game import PointUtils
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.Entities import *
from PythonClientAPI.libs.Game.World import *
import math

class PlayerAI:

    #Class data structures
    prev_goal = [None, None, None, None]
    goal_reached = [False,False,False,False]

    def __init__(self):
        pass

    # Returns closest locs for a friendly unit in a list. Each list contains the ordering of tuples that are closest to set of point
    def closest_loc_finder(self, pickups, world, friendly_unit):

        # Empty List Check
        if (len(pickups) == 0):
            return []

        #Acquire unit's position and make a distance list
        unit_pos = friendly_unit.position

        dist_list = []
        for pickup in pickups:
            dist = world.get_path_length(unit_pos, pickup)  # Get distance between current position and pickup
            dist_list.append(dist)

        # Merge the two lists and sort it (default sort sorts by second elem)
        combined_list = list(zip(pickups, dist_list))
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
        #In this version, the bots move to collect powerups and then hold a control point.
        #Optimized!

        #Obtain all power up locations
        pickups_laser_rifle = world.get_positions_of_pickup_type(PickupType.WEAPON_LASER_RIFLE)
        pickups_rail_gun = world.get_positions_of_pickup_type(PickupType.WEAPON_RAIL_GUN)
        pickups_mini_blaster = world.get_positions_of_pickup_type(PickupType.WEAPON_MINI_BLASTER)
        pickups_scatter_gun = world.get_positions_of_pickup_type(PickupType.WEAPON_SCATTER_GUN)
        pickups_shield = world.get_positions_of_pickup_type(PickupType.SHIELD)
        pickups_repair_kit = world.get_positions_of_pickup_type(PickupType.REPAIR_KIT)

        ##print(len(pickups_laser_rifle))
        ##print(len(pickups_rail_gun))
        ##print(len(pickups_mini_blaster))
        ##print(len(pickups_scatter_gun))
        ##print(len(pickups_shield))
        ##print(len(pickups_repair_kit))

        # Aggregate all existing pickups into single list
        pickups = pickups_laser_rifle + pickups_rail_gun + pickups_mini_blaster + pickups_scatter_gun + pickups_shield + pickups_repair_kit

        #Sorted pickups is a list of lists
        sorted_pickups = []
        sorted_pickups_0 = self.closest_loc_finder(pickups, world, friendly_units[0])
        sorted_pickups.append(sorted_pickups_0)
        sorted_pickups_1 = self.closest_loc_finder(pickups, world, friendly_units[1])
        sorted_pickups.append(sorted_pickups_1)
        sorted_pickups_2 = self.closest_loc_finder(pickups, world, friendly_units[2])
        sorted_pickups.append(sorted_pickups_2)
        sorted_pickups_3 = self.closest_loc_finder(pickups, world, friendly_units[3])
        sorted_pickups.append(sorted_pickups_3)

        #Simple program to obtain all available powerups
        for i in range(0,4): #Runs once per friendly unit

            unit = friendly_units[i]
            unit_pos = unit.position

            print("Unit:",i)
            #print("Position:",unit_pos)

            print(sorted_pickups[i])

            # Iterate through other bots' goals and remove their prev_dest from your sorted_pickups
            removables = list(range(0, 4))
            removables.remove(i)

            for removable in removables:
                if (self.prev_goal[removable] in sorted_pickups[i]):
                    sorted_pickups[i].remove(self.prev_goal[removable])

            print(sorted_pickups[i])

            #If list of pickups isn't empty ...
            if (sorted_pickups[i] != []):
                print("in if")

                if (self.prev_goal[i] == None):
                    pickup_loc = sorted_pickups[i][0]
                    self.prev_goal[i] = sorted_pickups[i][0]
                    #print("Initialized bot_prev_dest[i]",self.prev_goal[i])
                elif ((self.goal_reached[i]) and (len(sorted_pickups[i])) > 0):
                    pickup_loc = sorted_pickups[i][0] #sorted_pickups[i] indexes an individual sorted_pickups list!
                    self.prev_goal[i] = sorted_pickups[i][0]
                    self.goal_reached[i] = False
                    #print("Pickup Location Set:", pickup_loc)
                else:
                    pickup_loc = self.prev_goal[i] #Do not update state/flag since it remains the same
                    #print("Pickup Location Remains the Same!")


            else: #Otherwise, all pickups are currently being tracked, so go get your pickup
                print("in else")
                closest_point = world.get_nearest_control_point(unit_pos)
                pickup_loc = closest_point.position

            #print(pickup_loc)

            if (pickup_loc == unit_pos):
                unit.pickup_item_at_position()
                self.goal_reached[i] = True #Set goal flag
            else:
                unit.move_to_destination(pickup_loc)

            #if (unit)








