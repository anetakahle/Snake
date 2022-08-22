insert into ClientLayerDataTypes (id, name) values (1, 'weights');
insert into ClientLayerDataTypes (id, name) values (2, 'biases');

insert into GameEndReasons (id, name) values (1, 'outside of bounds');
insert into GameEndReasons (id, name) values (2, 'self collision');
insert into GameEndReasons (id, name) values (3, 'loop detected');
insert into GameEndReasons (id, name) values (4, 'out of moves');
insert into GameEndReasons (id, name) values (5, 'win');

insert into Commands (id, name) values (-1, 'unknown');
insert into Commands (id, name) values (0, 'spawn object');
insert into Commands (id, name) values (1, 'client move');
insert into Commands (id, name) values (2, 'destroy object');
insert into Commands (id, name) values (3, 'set property');
insert into Commands (id, name) values (4, 'call method');
insert into Commands (id, name) values (5, 'game end');
