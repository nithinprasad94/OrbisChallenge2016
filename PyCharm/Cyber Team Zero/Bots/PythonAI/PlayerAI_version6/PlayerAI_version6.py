from PythonClientAPI.libs.Game import PointUtils
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.Entities import *
from PythonClientAPI.libs.Game.World import *
import math
import random

class PlayerAI:

    #Class data structures
    # - aggregate history of previous 3 turns - sense/reason using prev 3 turns and only update history after reasoning
    world_map = []
    turn_count = 0
    #prev_actions_taken = [[],[],[],[]] #Updates current action before actuation
    position_history = [[],[],[],[]]
    enemy_position_history = [[],[],[],[]]
    map_type = None
    ideal_weapon_roster = []

    def __init__(self):
        pass

    # Returns closest items for a source in a list. Each list contains the ordering of tuples that are closest to set of point
    def closest_loc_finder(self, source, items, world, friendly_unit): #Source says where to start from ...

        #Increment turn count by 1
        self.turn_count += 1

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

    def obtain_closest_objectives(self, world, enemy_units, friendly_units, sorted_pickups, control_points, main_frames):

        params_list = []
        for i in range(0,4):

            #Get the closest mainframe
            if main_frames != []:
                main_frame_positions = [main_frame.position for main_frame in main_frames]
                sorted_main_frames = self.closest_loc_finder(friendly_units[i].position,main_frame_positions,world,friendly_units[i])

                for main_frame in sorted_main_frames:
                    if (main_frame.controlling_team != friendly_units[i].team):
                        target_loc = main_frame.position
                        param = ("move_towards_main_frame",i,target_loc)
                        params_list.append(param)

            control_point_positions = []
            for control_point in control_points:
                control_point_positions.append(control_point.position)
            sorted_control_points = self.closest_loc_finder(friendly_units[i].position,control_point_positions,world,
                                                         friendly_units[i])
            j = 0
            for control_point in sorted_control_points:
                if (control_point.controlling_team != friendly_units[i].team):
                    target_loc = control_point.position
                    param = ("move_towards_control_point",i,target_loc)
                    params_list.append(param)
                j += 1

            else:
                param = ("no_points_to_move_towards",-1,(-1,-1)) #(-1,-1) corresponds to invalid point (therefore ignore)
                params_list.append(param)

        return params_list

    def obtain_optimum_objectives(self,world, enemy_units, friendly_units, sorted_pickups, control_points, main_frames):

        #Obtain weaponry of all friendlies
        weapons_list = [friendly_unit.current_weapon_type for friendly_unit in friendly_units]
        weapons_list_rem = weapons_list[:]

        #If weaponry is not optimum, set optimized_weaponry to False
        for weapon in self.ideal_weapon_roster:
            if weapon in weapons_list:
                weapons_list_rem.remove(weapon)

        optimized_weaponry = False
        num_unoptimized_weapons = len(weapons_list_rem)
        if len(weapons_list_rem) == 0:
            optimized_weaponry = True

        #If main frames exist, set main_frames_exist to True
        main_frames_exist = False
        if len(main_frames) > 0:
            main_frames_exist = True

        #If main frames need critical attention, set main_frames_critical to True
        main_frames_critical = False
        num_warning_main_frames = 0
        num_crit_main_frames = 0
        if not(main_frames_exist):
            pass #No code here
        else:
            for main_frame in main_frames:
                if (main_frame.controlling_team != friendly_units[0].team):
                    main_frames_critical = True
                    if (main_frame.controlling_team == enemy_units[0].team):
                        num_crit_main_frames += 1
                    else:
                        num_warning_main_frames += 1

        #If any uncaptured control points, set control_points_warning to True
        control_points_warning = False
        num_total_control_points = 0
        num_unowned_control_points = 0
        for control_point in control_points:
            num_total_control_points += 1
            if (control_point.controlling_team != friendly_units[0].team):
                num_unowned_control_points += 1
                control_points_warning = True

        #If any unobtained powerups on map, set unobtained_powerups to True
        unobtained_powerups = False
        num_unobtained_powerups = len(sorted_pickups[0]) #All indices of sorted pickups have same length of list of points!
        if (len(sorted_pickups[0]) > 0):
            unobtained_powerups = True

        #Separate Units
        unit_0 = friendly_units[0]
        unit_1 = friendly_units[1]
        unit_2 = friendly_units[2]
        unit_3 = friendly_units[3]

        #If you're getting shot at ... set unit_[x]_shot_at to True
        unit_0_shot_at = (unit_0.damage_taken_last_turn > 0)
        unit_1_shot_at = (unit_1.damage_taken_last_turn > 0)
        unit_2_shot_at = (unit_2.damage_taken_last_turn > 0)
        unit_3_shot_at = (unit_3.damage_taken_last_turn > 0)

        #if you can fire at a unit ... set unit_[x]_can_fire to True
        unit_0_can_fire = (unit_0.check_shot_against_enemy(enemy_units[0]) == ShotResult.CAN_HIT_ENEMY) or \
                    (unit_0.check_shot_against_enemy(enemy_units[1]) == ShotResult.CAN_HIT_ENEMY) or \
                          (unit_0.check_shot_against_enemy(enemy_units[2]) == ShotResult.CAN_HIT_ENEMY) or \
                           (unit_0.check_shot_against_enemy(enemy_units[3]) == ShotResult.CAN_HIT_ENEMY)
        unit_1_can_fire = (unit_1.check_shot_against_enemy(enemy_units[0]) == ShotResult.CAN_HIT_ENEMY) or \
                    (unit_1.check_shot_against_enemy(enemy_units[1]) == ShotResult.CAN_HIT_ENEMY) or \
                          (unit_1.check_shot_against_enemy(enemy_units[2]) == ShotResult.CAN_HIT_ENEMY) or \
                           (unit_1.check_shot_against_enemy(enemy_units[3]) == ShotResult.CAN_HIT_ENEMY)
        unit_2_can_fire = (unit_2.check_shot_against_enemy(enemy_units[0]) == ShotResult.CAN_HIT_ENEMY) or \
                    (unit_2.check_shot_against_enemy(enemy_units[1]) == ShotResult.CAN_HIT_ENEMY) or \
                          (unit_2.check_shot_against_enemy(enemy_units[2]) == ShotResult.CAN_HIT_ENEMY) or \
                           (unit_2.check_shot_against_enemy(enemy_units[3]) == ShotResult.CAN_HIT_ENEMY)
        unit_3_can_fire = (unit_3.check_shot_against_enemy(enemy_units[0]) == ShotResult.CAN_HIT_ENEMY) or \
                    (unit_3.check_shot_against_enemy(enemy_units[1]) == ShotResult.CAN_HIT_ENEMY) or \
                          (unit_3.check_shot_against_enemy(enemy_units[2]) == ShotResult.CAN_HIT_ENEMY) or \
                           (unit_3.check_shot_against_enemy(enemy_units[3]) == ShotResult.CAN_HIT_ENEMY)

        #Depending on previous answers, compute heuristics and determine bot allocation!
        # (Lowest Priority -> Highest Priority)

        optimized_weaponry_score = num_unoptimized_weapons*50 #50 = points per pickup

        main_frames_score = (num_warning_main_frames*200) + ((num_crit_main_frames*750)) #750 = 75 per turn * 10 turns estimate

        control_points_score = num_unowned_control_points*75

        power_up_score = num_unobtained_powerups*[20-self.turn_count]*50

        unit_0_status = ""
        unit_1_status = ""
        unit_2_status = ""
        unit_3_status = ""

        combat_free_list = [unit_0,unit_1,unit_2,unit_3]
        return_list = []

        if unit_0_shot_at or unit_0_can_fire:
            unit_0_status = "in_combat"
            combat_free_list.remove(unit_0)
            return_list.append((combat_0_status,0,(-1,-1)))
        if unit_1_shot_at or unit_1_can_fire:
            unit_1_status = "in_combat"
            combat_free_list.remove(unit_1)
            return_list.append((combat_1_status,1,(-1, -1)))
        if unit_2_shot_at or unit_2_can_fire:
            unit_2_status = "in_combat"
            combat_free_list.remove(unit_2)
            return_list.append((combat_2_status,2,(-1, -1)))
        if unit_3_shot_at or unit_3_can_fire:
            unit_3_status = "in_combat"
            combat_free_list.remove(unit_3)
            return_list.append((combat_3_status,3,(-1, -1)))

        num_bots_allocable = len(combat_free_list)

        if (num_bots_allocable == 0):
            return return_list

        else:
            priority_list = [(power_up_score) > 3000,(power_up_score > 1500),(main_frames_score >= 750),(control_points_score >= 225)]
            #ignore optimized weaponry for now
            priority_alloc_list = [3,1,2,1]
            desc_list = ["gather_powerup","gather_powerup","move_towards_main_frame","move_towards_control_point"]

            p_index = 0
            while(len(combat_free_list) > 0):
                priority = priority_list[p_index]
                if (priority):
                    if len(combat_free_list) >= priority_alloc_list[p_index]:
                        for j in range(priority_alloc_list[p_index]):
                            combat_free_list.remove(combat_free_list[0])
                            return_list.append(desc_list[p_index],4,(-1,-1)) #Return 4 to signify - use any bot!
                        priority_alloc_list[p_index] = 0
                p_index += 1

                #length cant be more than 4, so we're safe

        return return_list

    def actuate(self, world, enemy_units, friendly_units, list_of_directives, sorted_pickups, sorted_control_points, main_frames):

        odd_jobs = []
        avail_bots = [0,1,2,3]

        for directive in list_of_directives:
            (action,friendly_index,element) = directive

            if (friendly_index == 4): #Add odd_job to odd_jobs
                odd_jobs.append(action) #element is (-1,-1) for this, so it doesnt matter!

            elif (friendly_index == -1):
                #Do nothing - corresponds to an edge case
                pass

            elif (friendly_index in [0,1,2,3]):

                unit = friendly_units[friendly_index]
                if action == "move_towards_main_frame" or action == "move_towards_control_point":
                    pickup_loc = element
                    if (pickup_loc == unit.position):
                        unit.pickup_item_at_position()
                    else:
                        unit.move_to_destination(pickup_loc)
                    avail_bots.remove(friendly_index)

                elif action == "in_combat": #element is (-1,-1) -> doesn't matter

                    unit_weapon = unit.current_weapon_type
                    enemy = enemy_units[friendly_index]

                    enemy_weapon = enemy.current_weapon_type

                    unit_weapon_range = unit_weapon.get_range()
                    unit_weapon_damage = unit_weapon.get_damage()
                    enemy_weapon_range = enemy_weapon.get_range()
                    enemy_weapon_damage = enemy_weapon.get_damage()

                    can_shoot_target = world.can_shooter_shoot_target(unit.position, enemy.position, unit_weapon_range)

                    if (can_shoot_target):
                        unit.shoot_at(enemy)
                    else:
                        pass  # Want to run otherwise ...

        while len(avail_bots) > 0:
            i = avail_bots[0]
            unit = friendly_units[i]
            job = odd_jobs[0]

            if (job == "gather_power_up"):
                if (sorted_pickups[i] != []):

                    pickup_loc = sorted_pickups[i][0]

            elif (job == "move_towards_main_frame"):
                j = 0
                while (j < len(main_frames)):
                    closest_point = main_frames[j]
                    point_pos = closest_point.position
                    point_controlling_team = closest_point.controlling_team

                    if (point_controlling_team != friendly_units[i].team):
                        pickup_loc = point_pos

            elif (job == "move_towards_control_point"):
                j = 0
                while (j < len(sorted_pickups)):
                    closest_point = sorted_control_points[j]
                    point_pos = closest_point.position
                    point_controlling_team = closest_point.controlling_team

                    if (point_controlling_team != friendly_units[i].team):
                        pickup_loc = point_pos

            if (pickup_loc == unit.position):
                unit.pickup_item_at_position()
            else:
                unit.move_to_destination(pickup_loc)


    def update_history_lists(self, world, enemy_units, friendly_units):

        for i in range(0,4):
            if (len(self.position_history[i]) < 3):
                self.position_history[i].append(friendly_units[i].position)
                self.enemy_position_history[i].append(enemy_units[i].position)
            else:
                self.position_history[i].remove(self.position_history[i][0])
                self.position_history[i].append(friendly_units[i].position)
                self.enemy_position_history[i].remove(self.enemy_position_history[i][0])
                self.enemy_position_history[i].append(enemy_units[i].position)


    def do_move(self, world, enemy_units, friendly_units):
        """
        This method will get called every turn; Your glorious AI code goes here.
        
        :param World world: The latest state of the world.
        :param list[EnemyUnit] enemy_units: An array of all 4 units on the enemy team. Their order won't change.
        :param list[FriendlyUnit] friendly_units: An array of all 4 units on your team. Their order won't change.
        """

        ######VERSION INFO########
        #In this version, the bots learn to co-operate with each other to enhance performance!

        #Initialize map on first call to function!
        if (self.world_map == []):

            #Initialize world map and determine map type
            world_width = world.width
            world_height = world.height
            num_blocking_tiles = 0 #Number of tiles that block bullets/movement (belong to wall)
            num_tiles = 0
            num_wall_blocks = 0
            num_floor_blocks = 0
            for x in range(1,world_width-1): #Exclude outer walls for computation
                for y in range(1,world_height-1):
                    num_tiles += 1
                    tile = world.get_tile((x,y))
                    self.world_map.append(((x,y),tile))
                    if (tile == TileType.WALL):
                        num_wall_blocks += 1
                    if (tile == TileType.FLOOR):
                        num_floor_blocks += 1

            #State map type and weapon roster
            if (num_floor_blocks/num_wall_blocks) > 1.2:
                self.map_type = "mid_ranged"
                self.ideal_weapon_roster = [PickupType.WEAPON_RAIL_GUN,PickupType.WEAPON_RAIL_GUN,PickupType.WEAPON_LASER_RIFLE,PickupType.WEAPON_SCATTER_GUN]
            else:
                self.map_type = "close_quarters"
                self.ideal_weapon_roster = [PickupType.WEAPON_RAIL_GUN,PickupType.WEAPON_LASER_RIFLE,PickupType.WEAPON_LASER_RIFLE,PickupType.WEAPON_SCATTER_GUN]

        #Sense all relevant data from map
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

        #Get mainframes
        main_frames = []
        for control_point in control_points:
            if control_point.is_mainframe:
                main_frames.append(control_point)

        #All friendly and enemy units given directly (for now)

        ############MAKE SENSE OF THE WORLD AND HISTORY#############

        #If map was just initialized:
        if (self.position_history[0] == []): #By inference all other position history indices are also empty lists!

            list_of_directives = self.obtain_closest_objectives(world, enemy_units, friendly_units, sorted_pickups, control_points, main_frames)
            self.actuate(world,enemy_units,friendly_units,list_of_directives)
            self.update_history_lists(world,enemy_units,friendly_units)

        #Otherwise:
        else:
            list_of_directives = self.obtain_optimum_objectives(world, enemy_units, friendly_units, sorted_pickups, control_points, main_frames)
            self.actuate(world, enemy_units, friendly_units,list_of_directives)
            self.update_history_lists(world, enemy_units, friendly_units)