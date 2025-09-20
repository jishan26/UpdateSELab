#!/usr/bin/env python3
"""
Test script to demonstrate the live location tracking system.
This script simulates drivers sending location updates and shows how the system works.
"""

import asyncio
import websockets
import json
import random
import time
from datetime import datetime

# Test coordinates around a central location (e.g., a city center)
BASE_LAT = 22.345663
BASE_LNG = 91.82251

async def simulate_driver(driver_id, name, token):
    """Simulate a driver sending location updates."""
    uri = f"ws://127.0.0.1:8000/ws?token={token}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"🚑 Driver {name} (ID: {driver_id}) connected")
            
            # Send initial location
            lat = BASE_LAT + random.uniform(-0.01, 0.01)
            lng = BASE_LNG + random.uniform(-0.01, 0.01)
            
            initial_message = {
                "type": "add-location",
                "data": {
                    "driver_id": driver_id,
                    "latitude": lat,
                    "longitude": lng,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            await websocket.send(json.dumps(initial_message))
            print(f"📍 Driver {name} sent initial location: {lat:.6f}, {lng:.6f}")
            
            # Simulate movement for 30 seconds
            for i in range(6):  # 6 updates over 30 seconds
                await asyncio.sleep(5)  # Update every 5 seconds
                
                # Move slightly in a random direction
                lat += random.uniform(-0.001, 0.001)
                lng += random.uniform(-0.001, 0.001)
                
                update_message = {
                    "type": "update-location",
                    "data": {
                        "driver_id": driver_id,
                        "latitude": lat,
                        "longitude": lng,
                        "timestamp": datetime.now().isoformat()
                    }
                }
                
                await websocket.send(json.dumps(update_message))
                print(f"📍 Driver {name} updated location: {lat:.6f}, {lng:.6f}")
                
                # Listen for any responses
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    response_data = json.loads(response)
                    print(f"📨 Driver {name} received: {response_data.get('type', 'unknown')}")
                except asyncio.TimeoutError:
                    pass
                    
    except Exception as e:
        print(f"❌ Driver {name} error: {e}")

async def simulate_rider(rider_id, name, token):
    """Simulate a rider receiving driver locations."""
    uri = f"ws://127.0.0.1:8000/ws?token={token}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"👤 Rider {name} (ID: {rider_id}) connected")
            
            # Listen for driver location updates
            for i in range(10):  # Listen for 10 messages
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    response_data = json.loads(response)
                    
                    if response_data.get("type") == "nearby-drivers":
                        drivers = response_data.get("data", {})
                        print(f"🚑 Rider {name} sees {len(drivers)} nearby drivers")
                        for driver_id, driver_data in drivers.items():
                            print(f"   - Driver {driver_id}: {driver_data['latitude']:.6f}, {driver_data['longitude']:.6f}")
                    
                    elif response_data.get("type") == "driver-location":
                        driver_data = response_data.get("data", {})
                        print(f"🚑 Rider {name} received driver {driver_data['driver_id']} location: {driver_data['latitude']:.6f}, {driver_data['longitude']:.6f}")
                    
                    else:
                        print(f"📨 Rider {name} received: {response_data.get('type', 'unknown')}")
                        
                except asyncio.TimeoutError:
                    print(f"⏰ Rider {name} timeout waiting for messages")
                    break
                    
    except Exception as e:
        print(f"❌ Rider {name} error: {e}")

async def main():
    """Main test function."""
    print("🚀 Starting Live Location Tracking System Test")
    print("=" * 50)
    
    # Note: In a real test, you would need valid JWT tokens
    # For this demo, we'll assume the tokens are valid
    print("⚠️  Note: This test requires valid JWT tokens from your authentication system")
    print("   Make sure your FastAPI server is running on http://127.0.0.1:8000")
    print()
    
    # Simulate 3 drivers and 2 riders
    tasks = []
    
    # Add drivers
    for i in range(3):
        driver_id = i + 1
        name = f"Driver-{driver_id}"
        token = f"driver_token_{driver_id}"  # Replace with real token
        tasks.append(simulate_driver(driver_id, name, token))
    
    # Add riders
    for i in range(2):
        rider_id = i + 10
        name = f"Rider-{rider_id}"
        token = f"rider_token_{rider_id}"  # Replace with real token
        tasks.append(simulate_rider(rider_id, name, token))
    
    # Run all simulations concurrently
    await asyncio.gather(*tasks, return_exceptions=True)
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    print("Live Location Tracking System Test")
    print("Make sure your FastAPI server is running first!")
    print("Run: uvicorn FastAPI-demo.api:app --reload")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
