#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Modified for demo purposes.

Sensor synchronization example for CARLA

The communication model for the syncronous mode in CARLA sends the snapshot
of the world and the sensors streams in parallel.
We provide this script as an example of how to syncrononize the sensor
data gathering in the client.
To to this, we create a queue that is being filled by every sensor when the
client receives its data and the main loop is blocked until all the sensors
have received its data.
This suppose that all the sensors gather information at every tick. It this is
not the case, the clients needs to take in account at each frame how many
sensors are going to tick at each frame.
"""

import time
import glob
import os
import sys
from queue import Queue
from queue import Empty

try:
    sys.path.append(glob.glob('./carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

# waiting for the carla server, till now it is getting started..
#-----------------------------------------------------
import socket

def wait_for_carla(host, port, timeout=60):
    print(f"Waiting for CARLA server at {host}:{port}...")
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("CARLA server is up!")
                return
        except (ConnectionRefusedError, socket.timeout):
            if time.time() - start > timeout:
                raise TimeoutError("Timed out waiting for CARLA server.")
            time.sleep(2)
##----------------------------------------------------

import carla


# Sensor callback.
# This is where you receive the sensor data and
# process it as you liked and the important part is that,
# at the end, it should include an element into the sensor queue.
def sensor_callback(sensor_data, sensor_queue, sensor_name):
    # Do stuff with the sensor_data data like save it to disk
    # Then you just need to add to the queue
    sensor_queue.put((sensor_data.frame, sensor_name))


def main():
    # We start creating the client
    client = carla.Client('carla_server', 2000, worker_threads=8) # Carla running in a container, host name is the name of the container
    client.set_timeout(5.0)
    world = client.get_world()

    try:
        # We need to save the settings to be able to recover them at the end
        # of the script to leave the server in the same state that we found it.
        original_settings = world.get_settings()
        settings = world.get_settings()

        # We set CARLA syncronous mode
        settings.fixed_delta_seconds = 0.1
        settings.synchronous_mode = True
        world.apply_settings(settings)

        # We create the sensor queue in which we keep track of the information
        # already received. This structure is thread safe and can be
        # accessed by all the sensors callback concurrently without problem.
        sensor_queue = Queue()

        # Bluepints for the sensors
        blueprint_library = world.get_blueprint_library()

        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        radar_bp = blueprint_library.find('sensor.other.radar')

        # We create all the sensors and keep them in a list for convenience.
        sensor_list = []

        lidar_bp.set_attribute('points_per_second', '1000')
        lidar01 = world.spawn_actor(lidar_bp, carla.Transform())
        lidar01.listen(lambda data: sensor_callback(data, sensor_queue, "lidar01"))
        sensor_list.append(lidar01)

        radar01 = world.spawn_actor(radar_bp, carla.Transform())
        radar01.listen(lambda data: sensor_callback(data, sensor_queue, "radar01"))
        sensor_list.append(radar01)

        # Main loop
        while True:
            # Tick the server
            world.tick()
            w_frame = world.get_snapshot().frame
            print("\nWorld's frame: %d" % w_frame)

            # Now, we wait to the sensors data to be received.
            # As the queue is blocking, we will wait in the queue.get() methods
            # until all the information is processed and we continue with the next frame.
            # We include a timeout of 1.0 s (in the get method) and if some information is
            # not received in this time we continue.
            try:
                for _ in range(len(sensor_list)):
                    s_frame = sensor_queue.get(True, 1.0)
                    print("    Frame: %d   Sensor: %s" % (s_frame[0], s_frame[1]))

            except Empty:
                print("    Some of the sensor information is missed")

    finally:
        world.apply_settings(original_settings)
        for sensor in sensor_list:
            if sensor.is_listening:
                sensor.stop()
            sensor.destroy()


if __name__ == "__main__":
    print('running carla client...')
    try:
        wait_for_carla("carla_server", 2000)
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')
