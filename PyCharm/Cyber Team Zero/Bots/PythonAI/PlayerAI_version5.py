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
        #In this version, the bots finally get a brain! They attempt to use a state-machine to optimize power-up pickup,
        # detecting getting hit, and acquiring and eliminating enemies!. Mainframe Control is Prioritized!!!!

        #BRAIN!!!!!!

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

        #Accumulate all control points and their properties
        control_points = world.control_points
        control_point_positions = []
        for control_point in control_points:
            control_point_positions.append(control_point.position)

        #All friendly and enemy units given directly (for now)

        #Actuate Simple State Machine - initialize actions to None
        #bot_0_action = None
        #bot_1_action = None
        #bot_2_action = None
        #bot_3_action = None

        #Simple program to obtain all available powerups
        for i in range(0,4): #Runs once per friendly unit
            unit = friendly_units[i]

            prev_move_was_error = False

            print("Unit:", i)

            # Update position list
            if (len(self.position_history[i]) < 3):
                self.position_history[i].append(unit.position)
            else:
                self.position_history[i].remove(self.position_history[i][0])
                self.position_history[i].append(unit.position)

            # Threat-processing:
            # Are we getting shot at?
            if (unit.damage_taken_last_turn > 0):

                # Yes -> do we have shield?
                if (unit.num_shields > 0):

                    unit.activate_shield()

                # If not, can we duel them (1 or more adversaries)?
                else:

                    #Determine number of shooters
                    num_shooters = len(unit.get_last_turn_shooters())

                    #If number of shooters is > 1, run!
                    if num_shooters > 1:
                        #Attempt to run?
                        #For now, do nothing and die!
                        pass

                    #If not, determine weapon characteristics
                    else:
                        unit_weapon = unit.current_weapon_type
                        enemy = unit.get_last_turn_shooters()[0]
                        enemy_weapon = enemy.current_weapon_type

                        unit_weapon_range = unit_weapon.get_range()
                        unit_weapon_damage = unit_weapon.get_damage()
                        enemy_weapon_range = enemy_weapon.get_range()
                        enemy_weapon_damage = enemy_weapon.get_damage()

                        can_shoot_target = world.can_shooter_shoot_target(unit.position,enemy.position,unit_weapon_range)

                        if (can_shoot_target) and (unit_weapon_damage >= enemy_weapon_damage):
                            unit.shoot_at(enemy)
                        else:
                            pass #Want to run otherwise ...


            # Do we see an enemy in range who we can engage?
            elif (unit.check_shot_against_enemy(enemy_units[0]) == ShotResult.CAN_HIT_ENEMY) or \
                    (unit.check_shot_against_enemy(enemy_units[1]) == ShotResult.CAN_HIT_ENEMY) or \
                            unit.check_shot_against_enemy(enemy_units[2]) == ShotResult.CAN_HIT_ENEMY or \
                            unit.check_shot_against_enemy(enemy_units[3]) == ShotResult.CAN_HIT_ENEMY:
                #Acquire target
                enemy_target = None
                if unit.check_shot_against_enemy(enemy_units[0]) == ShotResult.CAN_HIT_ENEMY:
                    enemy_target = enemy_units[0]
                elif unit.check_shot_against_enemy(enemy_units[1]) == ShotResult.CAN_HIT_ENEMY:
                    enemy_target = enemy_units[1]
                elif unit.check_shot_against_enemy(enemy_units[2]) == ShotResult.CAN_HIT_ENEMY:
                    enemy_target = enemy_units[2]
                elif unit.check_shot_against_enemy(enemy_units[3]) == ShotResult.CAN_HIT_ENEMY:
                    enemy_target = enemy_units[3]

                unit.shoot_at(enemy_target)

            #Otherwise, process previous code?
            else:

                #Is there a powerup nearby?
                # If list of pickups isn't empty ...
                if (sorted_pickups[i] != []):

                    pickup_loc = sorted_pickups[i][0]

                # Is there a control point we can capture?
                else:  # Otherwise, all pickups are currently being tracked, so go get your pickup

                    # Get list of closest control points
                    sorted_control_point_positions = self.closest_loc_finder(friendly_units[i].position,
                                                                             control_point_positions, world,
                                                                             friendly_units[i])
                    sorted_control_points = []

                    cp_list_length = len(sorted_control_point_positions)
                    cp_index_1 = 0
                    cp_index_2 = 0
                    control_point_found = False
                    pickup_loc = None  # Declare it here since you're only assigning values in loops/if statements

                    for_count = 0
                    for cp_position in sorted_control_point_positions:

                        point_found = False

                        point_index = 0

                        while (not (point_found) and point_index < cp_list_length):
                            if (control_points[point_index].position == cp_position):
                                point_found = True
                                sorted_control_points.append(control_points[point_index])
                            point_index += 1
                        for_count += 1

                    # Find the closest control point to move to!
                    while ((cp_index_1 < cp_list_length) and not (control_point_found)):
                        closest_point = sorted_control_points[cp_index_1]
                        point_pos = closest_point.position
                        point_controlling_team = closest_point.controlling_team
                        point_is_main_frame = closest_point.is_mainframe

                        if (point_is_main_frame) and (point_controlling_team != friendly_units[i].team):
                            pickup_loc = point_pos
                            control_point_found = True

                        cp_index_1 += 1

                    while ((cp_index_2 < cp_list_length) and not (control_point_found)):
                        closest_point = sorted_control_points[cp_index_2]
                        point_pos = closest_point.position
                        point_controlling_team = closest_point.controlling_team
                        num_enemy_units = closest_point.get_num_enemy_units_around()

                        if (point_controlling_team == friendly_units[i].team):
                            pass  # Do nothing if point already controlled
                        else:
                            pickup_loc = point_pos
                            control_point_found = True

                        cp_index_2 += 1

                    # If all points have been controlled by your team, move to closest point!
                    if (cp_index_2 == cp_list_length):
                        pickup_loc = sorted_control_points[0].position

                #Do movement or take action?
                if (pickup_loc == unit.position):
                    unit.pickup_item_at_position()
                    self.goal_reached[i] = True  # Set goal flag
                else:
                    unit.move_to_destination(pickup_loc)







