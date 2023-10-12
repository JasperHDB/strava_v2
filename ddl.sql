create table users
(
    strava_athlete_id bigint not null
        primary key,
    firstname         varchar(255),
    lastname          varchar(255),
    refresh_token     text
);