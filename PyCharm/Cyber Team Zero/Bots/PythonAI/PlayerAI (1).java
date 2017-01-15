import java.util.ArrayList;

import com.orbischallenge.ctz.Constants;
import com.orbischallenge.ctz.objects.ControlPoint;
import com.orbischallenge.ctz.objects.EnemyUnit;
import com.orbischallenge.ctz.objects.FriendlyUnit;
import com.orbischallenge.ctz.objects.Pickup;
import com.orbischallenge.ctz.objects.World;
import com.orbischallenge.ctz.objects.enums.MoveResult;
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
	final int INFINITY = 100000000;
	Point f0;
	Point f1;
	Point f2;
	Point f3;
	boolean toShoot;
	
	int min0;
	int idx0;
	int min1;
	int idx1;
	int min2;
	int idx2;
	int min3;
	int idx3;
	
	Point[] m = new Point[4];
	Point[] e = new Point[4];
    
	public PlayerAI() {
    	init = 0;
    	toShoot = false;
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
    		toShoot = false;
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
        	int j=0;
    		if(allCtrlPts.length>0){
    			toShoot = false;
    			for(int i =0; i < allCtrlPts.length; i++){
    				if(allCtrlPts[i].getControllingTeam().equals(friendlyUnits[0].getTeam())){
    					continue;
    				}
    				else{
    					j++;
    				}
    				
    			}
    		}
			if(j>0){
				toShoot = false;
    			f0 = friendlyUnits[0].getPosition();
    	    	
    	    	for(int i = 0; i < allCtrlPts.length; i++){
    	    		if(allCtrlPts[i].getControllingTeam().equals(friendlyUnits[0].getTeam()))
    	    			continue;
    	    		p0 = world.getPathLength(f0,allCtrlPts[i].getPosition());
    	    		if(p0<dist0){
    	    			index0 = i;
    	    			dist0 = p0;
    	    		}
    	    	}
    	    	m0 = allCtrlPts[index0].getPosition();
    	    	
    	    	f1 = friendlyUnits[1].getPosition();
    	    	
    	    	for(int i = 0; i < allCtrlPts.length; i++){
    	    		if(allCtrlPts[i].getControllingTeam().equals(friendlyUnits[0].getTeam()))
    	    			continue;
    	    		p1 = world.getPathLength(f1,allCtrlPts[i].getPosition());
    	    		if((p1<dist1)&&(index0 != i)){
    	    			index1 = i;
    	    			dist1 = p1;
    	    		}
    	    	}
    	    	m1 = allCtrlPts[index1].getPosition(); 	
    	    	
    			f2 = friendlyUnits[2].getPosition();
    	    	for(int i = 0; i < allCtrlPts.length; i++){
    	    		if(allCtrlPts[i].getControllingTeam().equals(friendlyUnits[0].getTeam()))
    	    			continue;
    	    		p2 = world.getPathLength(f2,allCtrlPts[i].getPosition());
    	    		if((p2<dist1)&&(index0 != i)&&(index1 != i)){
    	    			index2 = i;
    	    			dist2 = p2;
    	    		}
    	    	}
    	    	m2 = allCtrlPts[index2].getPosition();
    	    	
    	    	f3 = friendlyUnits[3].getPosition();
    	    	
    	    	for(int i = 0; i < allCtrlPts.length; i++){
    	    		if(allCtrlPts[i].getControllingTeam().equals(friendlyUnits[0].getTeam()))
    	    			continue;
    	    		p3 = world.getPathLength(f3,allCtrlPts[i].getPosition());
    	    		if((p3<dist1)&&(index0 != i)&&(index1 != i)&&(index2 != i)){
    	    			index3 = i;
    	    			dist3 = p3;
    	    		}
    	    	}
    	    	m3 = allCtrlPts[index3].getPosition();
			}
			else{
				toShoot = true;
				
				int[] d0 = new int[4];
				int[] d1 = new int[4];
				int[] d2 = new int[4];
				int[] d3 = new int[4];
				
				
				
				for(int i = 0; i < enemyUnits.length; i++){
					e[i] = enemyUnits[i].getPosition(); 
					d0[i] = world.getPathLength(friendlyUnits[0].getPosition(), e[i]);
					d1[i] = world.getPathLength(friendlyUnits[1].getPosition(), e[i]);
					d2[i] = world.getPathLength(friendlyUnits[2].getPosition(), e[i]);
					d3[i] = world.getPathLength(friendlyUnits[3].getPosition(), e[i]);
				}
				
				min0 = INFINITY;
				//idx0 = 0;
				for(int i = 0; i < enemyUnits.length; i++){
					if(enemyUnits[i].getHealth() <= 0)
						continue;
					if(d0[i]<min0){
						min0 = d0[i];
						idx0 = i;
					}    					
				}
				m0 = e[idx0];
				
				min1 = INFINITY;// = d1[0];
//				idx1 = 0;
				for(int i = 0; i < enemyUnits.length; i++){
					if(enemyUnits[i].getHealth() <= 0)
						continue;
					if((d1[i]<min1)){
						min1 = d1[i];
						idx1 = i;
					}    					
				}
				m1 = e[idx1];
				
				min2 = INFINITY;//d2[0];
//				idx2 = 0;
				for(int i = 0; i < enemyUnits.length; i++){
					if(enemyUnits[i].getHealth() <= 0)
						continue;
					if((d2[i]<min2)){
						min2 = d2[i];
						idx2 = i;
					}    					
				}
				m2 = e[idx2];
				
				min3 = INFINITY;// = d3[0];
//				idx3 = 0;
				for(int i = 0; i < enemyUnits.length; i++){
					if(enemyUnits[i].getHealth() <= 0)
						continue;
					if((d3[i]<min3)){
						min3 = d3[i];
						idx3 = i;
					}    					
				}
				m3 = e[idx3];
				
			}
    	}
    		
    	
//    	if((friendlyUnits[0].getLastMoveResult() == MoveResult.BLOCKED_BY_ENEMY)||(friendlyUnits[0].getLastMoveResult() == MoveResult.BLOCKED_BY_FRIENDLY)||
//    			(friendlyUnits[1].getLastMoveResult() == MoveResult.BLOCKED_BY_ENEMY)||(friendlyUnits[1].getLastMoveResult() == MoveResult.BLOCKED_BY_FRIENDLY)||	
//    			(friendlyUnits[2].getLastMoveResult() == MoveResult.BLOCKED_BY_ENEMY)||(friendlyUnits[2].getLastMoveResult() == MoveResult.BLOCKED_BY_FRIENDLY)||
//    			(friendlyUnits[3].getLastMoveResult() == MoveResult.BLOCKED_BY_ENEMY)||(friendlyUnits[3].getLastMoveResult() == MoveResult.BLOCKED_BY_FRIENDLY)){
    	if(init!=0 && (friendlyUnits[0].getLastMoveResult() != MoveResult.MOVE_COMPLETED)&&
    			(friendlyUnits[1].getLastMoveResult() != MoveResult.MOVE_COMPLETED)&&
    			(friendlyUnits[2].getLastMoveResult() != MoveResult.MOVE_COMPLETED)&&
    			(friendlyUnits[3].getLastMoveResult() != MoveResult.MOVE_COMPLETED)){
    		System.out.println(friendlyUnits[0].getLastMoveResult());
    		System.out.println(friendlyUnits[1].getLastMoveResult());
    		System.out.println(friendlyUnits[2].getLastMoveResult());
    		System.out.println(friendlyUnits[3].getLastMoveResult());
    		System.out.println("Length: " + enemyUnits.length);
    		System.out.println(m0 + "::" + m1 + "::" + m2 + "::" + m3);
    		Point origin = new Point(1,1);
    		friendlyUnits[0].move(origin);
    		friendlyUnits[1].move(origin);
    		friendlyUnits[2].move(origin);
    		friendlyUnits[3].move(origin);
    	}
    	else{
    		init++;
	    	if((friendlyUnits[0].getPosition().equals(m0)&&(allPickups.length>0)&&(toShoot==false))){
	    		friendlyUnits[0].pickupItemAtPosition();
	    	}
	    	else{
	    		if(toShoot == true){
	    			if(min0 < friendlyUnits[0].getCurrentWeapon().getRange()){
	    				friendlyUnits[0].shootAt(enemyUnits[idx0]);
	    			}
	    			else{
	    				friendlyUnits[0].move(m0);
	    			}
	    		}
	    		else{
	    			friendlyUnits[0].move(m0);
	    		}
	    	}
	    	
	    	if(friendlyUnits[1].getPosition().equals(m1)&&(toShoot==false)){
	    		friendlyUnits[1].pickupItemAtPosition();
	    	}
	    	else{
	    		if(toShoot == true){
	    			if(min1 < friendlyUnits[1].getCurrentWeapon().getRange()){
	    				friendlyUnits[1].shootAt(enemyUnits[idx1]);
	    			}
	    			else{
	    				friendlyUnits[1].move(m1);
	    			}
	    		}
	    		else{
	    			friendlyUnits[1].move(m1);
	    		}
	    	}
	    	
	    	if(friendlyUnits[2].getPosition().equals(m2)&&(toShoot==false)){
	    		friendlyUnits[2].pickupItemAtPosition();
	    	}
	    	else{
	    		if(toShoot == true){
	    			if(min2 < friendlyUnits[2].getCurrentWeapon().getRange()){
	    				friendlyUnits[2].shootAt(enemyUnits[idx2]);
	    			}
	    			else{
	    				friendlyUnits[2].move(m2);
	    			}
	    		}
	    		else{
	    			friendlyUnits[2].move(m2);
	    		}
	    	}
	    	
	    	if(friendlyUnits[3].getPosition().equals(m3)&&(toShoot==false)){
	    		friendlyUnits[3].pickupItemAtPosition();
	    	}
	    	else{
	    		if(toShoot == true){
	    			if(min3 < friendlyUnits[3].getCurrentWeapon().getRange()){
	    				friendlyUnits[3].shootAt(enemyUnits[idx3]);
	    			}
	    			else{
	    				friendlyUnits[3].move(m3);
	    			}
	    		}
	    		else{
	    			friendlyUnits[3].move(m3);
	    		}
	    	}
    	}
    }
}
