from dronekit import connect, VehicleMode
import time

# Connect to the drone
vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

# Target coordinates for landing
target_latitude = 0.0  # Replace with the desired latitude
target_longitude = 0.0  # Replace with the desired longitude

# Battery thresholds
takeoff_threshold = 95  # Percentage battery level to trigger takeoff
landing_threshold = 30  # Percentage battery level to trigger landing

def monitor_battery():
    """Get the current battery level of the drone."""
    return vehicle.battery.level

def takeoff():
    """Initiate takeoff."""
    print("Taking off...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    vehicle.simple_takeoff(10)  # Takeoff to 10 meters altitude

def land():
    """Initiate landing at the target coordinates."""
    print("Landing at target coordinates...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.simple_goto(target_latitude, target_longitude)
    time.sleep(10)  # Let it reach the target location
    vehicle.mode = VehicleMode("LAND")

# Main loop
while True:
    try:
        # Monitor battery level
        battery = monitor_battery()
        
        if battery >= takeoff_threshold:
            takeoff()
        elif battery <= landing_threshold:
            land()
        
        # Add some delay to avoid continuous checking
        time.sleep(10)
    
    except KeyboardInterrupt:
        print("Program terminated by user.")
        break
    except Exception as e:
        print("An error occurred:", str(e))