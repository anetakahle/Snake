create table if not exists Clients
(
    id integer primary key,
    name text
);

create table if not exists ClientGenerations
(
  id integer primary key,
  clientId integer not null,
  [index] integer not null,

  foreign key (clientId) references Clients (id)
);

create table if not exists ClientLayers
(
    id integer primary key,
    [index] integer not null,
    clientId integer not null,
    [name] text not null,

    foreign key (clientId) references Clients (id)
);

create table if not exists ClientLayerDataTypes
(
    id integer not null,
    [name] text not null
);

create table if not exists ClientLayerData
(
    id integer primary key,
    typeId integer not null,
    [data] text not null,
    layerId integer not null,

    foreign key (typeId) references ClientLayerDataTypes (id),
    foreign key (layerId) references ClientLayers (id)
);

create table if not exists GameEndReasons
(
    id integer not null,
    [name] text not null
);

create table if not exists ClientGenerationAgents
(
    id integer primary key,
    runtimeId text,
    clientGenerationId integer,

    foreign key (clientGenerationId) references ClientGenerations (id)
);

create table if not exists Games
(
    id integer primary key,
    runtimeId text not null,
    clientId integer not null,
    clientGenerationAgentId integer not null,
    [data] text not null,
    dateStart text not null,
    dateEnd text not null,
    score integer not null,
    moves integer not null,
    endReason integer not null,

    foreign key (clientId) references Clients (id),
    foreign key (clientGenerationAgentId) references ClientGenerationAgents (id),
    foreign key (endReason) references GameEndReasons (id)
);

create table if not exists Commands
(
    id integer not null,
    [name] text not null
);

create table if not exists GameCommands
(
    id integer primary key,
    gameId integer not null,
    commandId integer not null,
    [index] integer not null,
    [data] text not null,
    [date] text not null,

    foreign key (commandId) references Commands (id),
    foreign key (gameId) references Games (id)
);


