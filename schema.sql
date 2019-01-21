CREATE TABLE bug(
    bugId       INT PRIMARY KEY ASC,
    deviceId    INT NOT NULL,
    testerId    INT NOT NULL,
    FOREIGN KEY(deviceId) REFERENCES device(deviceId),
    FOREIGN KEY(testerId) REFERENCES tester(testerId)
);

CREATE TABLE device(
    deviceId       INT PRIMARY KEY ASC,
    description    TEXT
);

CREATE TABLE tester_device(
    testerId       INT NOT NULL,
    deviceId       INT NOT NULL,
    PRIMARY KEY (testerId, deviceId),
    FOREIGN KEY(testerId) REFERENCES tester(testerId),
    FOREIGN KEY(deviceId) REFERENCES device(deviceId)
);

CREATE TABLE tester(
    testerId       INT PRIMARY KEY ASC,
    firstName      TEXT,
    lastName       TEXT,
    country        TEXT,
    lastLogin      TEXT  --SQLite doesn't support DATETIME types
);

-- This could be cached for performance
CREATE VIEW tester_experience
AS
  SELECT tester.testerid,
         (SELECT Count(bug.bugid)
          FROM   bug
          WHERE  bug.testerid = tester.testerid) AS experience
  FROM  tester;

-- For data import.
-- Comment this out, if only using for schema
.mode csv
.import bugs.csv bug
.import devices.csv device
.import tester_device.csv tester_device
.import testers.csv tester
