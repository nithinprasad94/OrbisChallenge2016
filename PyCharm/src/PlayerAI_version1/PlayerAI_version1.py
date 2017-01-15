from PythonClientAPI.libs.Game import PointUtils
from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.Entities import *
from PythonClientAPI.libs.Game.World import *


class PlayerAI:
    def __init__(self):
        pass

    def do_move(self, world, enemy_units, friendly_units):
        """
        This method will get called every turn; Your glorious AI code goes here.
        
        :param World world: The latest state of the world.
        :param list[EnemyUnit] enemy_units: An array of all 4 units on the enemy team. Their order won't change.
        :param list[FriendlyUnit] friendly_units: An array of all 4 units on your team. Their order won't change.
        """

        ######VERSION INFO########
        #In this version, the bots move to collect powerups and then hold a control point.
        #Unoptimized!

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

        #Simple program to obtain all available powerups
        for i in range(0,4): #Runs once per friendly unit

            unit = friendly_units[i]
            unit_pos = friendly_units[i].position

            #pickup_loc = (3,3) #Some default value
            if len(pickups_laser_rifle) != 0:
                pickup_loc = pickups_laser_rifle[0]
                pickups_laser_rifle = pickups_laser_rifle[1:]
            elif len(pickups_rail_gun) != 0:
                pickup_loc = pickups_rail_gun[0]
                pickups_rail_gun = pickups_rail_gun[1:]
            elif len(pickups_mini_blaster) != 0:
                pickup_loc = pickups_mini_blaster[0]
                pickups_mini_blaster = pickups_mini_blaster[1:]
            elif len(pickups_scatter_gun) != 0:
                pickup_loc = pickups_scatter_gun[0]
                pickups_scatter_gun = pickups_scatter_gun[1:]
            elif len(pickups_shield) != 0:
                pickup_loc = pickups_shield[0]
                pickups_shield = pickups_shield[1:]
            elif len(pickups_repair_kit) != 0:
                #print("here")
                pickup_loc = pickups_repair_kit[0]
                pickups_repair_kit = pickups_repair_kit[1:]
            else: #Otherwise, all pickups are currently being tracked, so go get your pickup
                closest_point = world.get_nearest_control_point(unit_pos)
                pickup_loc = closest_point.position
                if pickup_loc == None:
                    print("omg it was None")
                    pickup_loc = (3,3)

            print(pickup_loc)

            if (pickup_loc == unit_pos):
                unit.pickup_item_at_position()
            else:
                unit.move_to_destination(pickup_loc)

            #if (unit)


