#! /usr/bin/python3

import sqlite3
import sys
import bme280
import smbus2


def bme280_data():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    return data


if __name__ == '__main__':
    data = bme280_data()

    # open the database
    conn = sqlite3.connect('/home/pi/Pi-Temp/bme280_data.db')
    curs = conn.cursor()

    # create tables if currently do not exist
    curs.execute("CREATE TABLE IF NOT EXISTS temperature "
                    "(id integer PRIMARY KEY AUTOINCREMENT, "
                    "timestamp datetime, "
                    "value numeric);")

    curs.execute("CREATE TABLE IF NOT EXISTS humidity "
                    "(id integer PRIMARY KEY AUTOINCREMENT, "
                    "timestamp datetime, "
                    "value numeric);")

    curs.execute("CREATE TABLE IF NOT EXISTS pressure "
                    "(id integer PRIMARY KEY AUTOINCREMENT, "
                    "timestamp datetime, "
                    "value numeric);")

    # add acquired sensor data to the database
    curs.execute("INSERT INTO temperature "
                "(timestamp, value) "
                "VALUES "
                "(datetime(CURRENT_TIMESTAMP, 'localtime'),?)", (data.temperature,))

    curs.execute("INSERT INTO humidity "
                "(timestamp, value) "
                "VALUES "
                "(datetime(CURRENT_TIMESTAMP, 'localtime'),?)", (data.humidity,))

    curs.execute("INSERT INTO pressure "
                "(timestamp, value) "
                "VALUES "
                "(datetime(CURRENT_TIMESTAMP, 'localtime'),?)", (data.pressure,))

    # close the database
    conn.commit()
    conn.close()
