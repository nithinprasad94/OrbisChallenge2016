import java.util.ArrayList;

import com.orbischallenge.ctz.Constants;
import com.orbischallenge.ctz.objects.ControlPoint;
import com.orbischallenge.ctz.objects.EnemyUnit;
import com.orbischallenge.ctz.objects.FriendlyUnit;
import com.orbischallenge.ctz.objects.Pickup;
import com.orbischallenge.ctz.objects.World;
import com.orbischallenge.ctz.objects.enums.PickupType;
import com.orbischallenge.game.engine.Point;


public class PlayerAI {

	Pickup[] allPickups;
	Point[] allRepairKits;
	Point[] allShields;
	Point[] allLasers;
	Point[] allMini;
	Point[] allRail;
	Point[] allScatter;
	ControlPoint[] allCtrlPts;
	int init;
	int INFINITY = 100000000;
	Point f0;
	Point f1;
	Point f2;
	Point f3;
	
    public PlayerAI() {
    	init = 0;
		//Any initialization code goes here.
    	
    }

	/**
	 * This method will get called every turn.
	 *
	 * @param world The latest state of the world.
	 * @param enemyUnits An array of all 4 units on the enemy team. Their order won't change.
	 * @param friendlyUnits An array of all 4 units on your team. Their order won't change.
	 */
    public void doMove(World world, EnemyUnit[] enemyUnits, FriendlyUnit[] friendlyUnits) {
		//Your glorious AI code goes here.
    	
		allPickups = world.getPickups();
    	
		allRepairKits = world.getPositionsOfPickupType(PickupType.REPAIR_KIT);
    	allShields = world.getPositionsOfPickupType(PickupType.SHIELD);
    	allLasers = world.getPositionsOfPickupType(PickupType.WEAPON_LASER_RIFLE);
    	allMini = world.getPositionsOfPickupType(PickupType.WEAPON_MINI_BLASTER);
    	allRail = world.getPositionsOfPickupType(PickupType.WEAPON_LASER_RIFLE);
    	allScatter = world.getPositionsOfPickupType(PickupType.WEAPON_RAIL_GUN);
    	
    	allCtrlPts = world.getControlPoints();
    	
    	int p0,p1,p2,p3;
    	Point m0,m1,m2,m3;
    	m0 = friendlyUnits[0].getPosition();
    	m1 = friendlyUnits[1].getPosition();
    	m2 = friendlyUnits[2].getPosition();
    	m3 = friendlyUnits[3].getPosition();
    	int index0=0, index1=0, index2=0, index3=0;
    	int dist0=INFINITY, dist00=INFINITY, dist1=INFINITY, dist11=INFINITY, dist2=INFINITY, dist22=INFINITY, dist3=INFINITY, dist33=INFINITY, dist4=INFINITY, dist44=INFINITY;
    	
    	if(allPickups.length>0){
	    	f0 = friendlyUnits[0].getPosition();
	    	
	    	for(int i = 0; i < allPickups.length; i++){
	    		p0 = world.getPathLength(f0,allPickups[i].getPosition());
	    		if(p0<dist0){
	    			index0 = i;
	    			dist0 = p0;
	    		}
	    	}
	    	m0 = allPickups[index0].getPosition();
	    	    	
	    	f1 = friendlyUnits[1].getPosition();
	    	
	    	for(int i = 0; i < allPickups.length; i++){
	    		p1 = world.getPathLength(f1,allPickups[i].getPosition());
	    		if((p1<dist1)&&(index0 != i)){
	    			index1 = i;
	    			dist1 = p1;
	    		}
	    	}
	    	m1 = allPickups[index1].getPosition(); 	
	    	
			f2 = friendlyUnits[2].getPosition();
	    	for(int i = 0; i < allPickups.length; i++){
	    		p2 = world.getPathLength(f2,allPickups[i].getPosition());
	    		if((p2<dist1)&&(index0 != i)&&(index1 != i)){
	    			index2 = i;
	    			dist2 = p2;
	    		}
	    	}
	    	m2 = allPickups[index2].getPosition();
	    	
	    	f3 = friendlyUnits[3].getPosition();
	    	
	    	for(int i = 0; i < allPickups.length; i++){
	    		p3 = world.getPathLength(f3,allPickups[i].getPosition());
	    		if((p3<dist1)&&(index0 != i)&&(index1 != i)&&(index2 != i)){
	    			index3 = i;
	    			dist3 = p3;
	    		}
	    	}
	    	m3 = allPickups[index3].getPosition();    	
		
    	}
    	else{
        	index0=index1=index2=index3=0;
        	dist0 = dist00 = dist1 = dist11 = dist2 = dist22 = dist3 = dist33=INFINITY;
    		if(allCtrlPts.length>0){
    			int j=0;
    			for(int i =0; i < allCtrlPts.length; i++){
    				if(allCtrlPts[i].getControllingTeam().equals(friendlyUnits[0].getTeam())){
    					continue;
    				}
    				else{
    					j++;
    				}
    				
    			}
    			if(j>0){
	    			f0 = friendlyUnits[0].getPosition();
	    	    	
	    	    	for(int i = 0; i < allCtrlPts.length; i++){
	    	    		p0 = world.getPathLength(f0,allCtrlPts[i].getPosition());
	    	    		if(p0<dist0){
	    	    			index0 = i;
	    	    			dist0 = p0;
	    	    		}
	    	    	}
	    	    	m0 = allCtrlPts[index0].getPosition();
	    	    	
	    	    	f1 = friendlyUnits[1].getPosition();
	    	    	
	    	    	for(int i = 0; i < allCtrlPts.length; i++){
	    	    		p1 = world.getPathLength(f1,allCtrlPts[i].getPosition());
	    	    		if((p1<dist1)&&(index0 != i)){
	    	    			index1 = i;
	    	    			dist1 = p1;
	    	    		}
	    	    	}
	    	    	m1 = allCtrlPts[index1].getPosition(); 	
	    	    	
	    			f2 = friendlyUnits[2].getPosition();
	    	    	for(int i = 0; i < allCtrlPts.length; i++){
	    	    		p2 = world.getPathLength(f2,allCtrlPts[i].getPosition());
	    	    		if((p2<dist1)&&(index0 != i)&&(index1 != i)){
	    	    			index2 = i;
	    	    			dist2 = p2;
	    	    		}
	    	    	}
	    	    	m2 = allCtrlPts[index2].getPosition();
	    	    	
	    	    	f3 = friendlyUnits[3].getPosition();
	    	    	
	    	    	for(int i = 0; i < allCtrlPts.length; i++){
	    	    		p3 = world.getPathLength(f3,allCtrlPts[i].getPosition());
	    	    		if((p3<dist1)&&(index0 != i)&&(index1 != i)&&(index2 != i)){
	    	    			index3 = i;
	    	    			dist3 = p3;
	    	    		}
	    	    	}
	    	    	m3 = allCtrlPts[index3].getPosition();
    			}
    			else{
    				
    			}
    		
        	}
    	}
    		
    	
    	
    	if((friendlyUnits[0].getPosition().equals(m0)&&(allPickups.length>0))){
    		friendlyUnits[0].pickupItemAtPosition();
    	}
    	else{
    		friendlyUnits[0].move(m0);
    	}
    	
    	if(friendlyUnits[1].getPosition().equals(m1)){
    		friendlyUnits[1].pickupItemAtPosition();
    	}
    	else{
    		friendlyUnits[1].move(m1);
    	}
    	
    	if(friendlyUnits[2].getPosition().equals(m2)){
    		friendlyUnits[2].pickupItemAtPosition();
    	}
    	else{
    		friendlyUnits[2].move(m2);
    	}
    	
    	if(friendlyUnits[3].getPosition().equals(m3)){
    		friendlyUnits[3].pickupItemAtPosition();
    	}
    	else{
    		friendlyUnits[3].move(m3);
    	}
    }
}
