PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Users(
   username TEXT PRIMARY KEY NOT NULL,
   role TEXT NOT NULL
);
CREATE TABLE Devices(
   room TEXT PRIMARY KEY NOT NULL,
   public_key TEXT NOT NULL
);
CREATE TABLE RoomStatus(
   room TEXT PRIMARY KEY NOT NULL,
   temperature INT NOT NULL,
   wind_speed INT NOT NULL,
   mode TEXT NOT NULL,
   sweep BOOLEAN NOT NULL,
   is_on BOOLEAN NOT NULL,
   last_update TEXT NOT NULL
);
CREATE TABLE Reports(
   room TEXT NOT NULL,
   start_time TEXT NOT NULL,
   end_time TEXT NOT NULL,
   temperature INT NOT NULL,
   wind_speed INT NOT NULL,
   mode TEXT NOT NULL,
   sweep BOOLEAN NOT NULL,
   duration INT NOT NULL,
   cost INT NOT NULL,
   PRIMARY KEY (room, start_time),
   FOREIGN KEY (room) REFERENCES RoomStatus(room)
);
COMMIT;
