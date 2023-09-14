# Weather Narratives

Noun, Adjective, temporal statement about a weather phenomena which either we have no measurements for or we wish to keep a subjective narrative.

There are 4 phenomena "nouns":
+ Temperature
+ Sky
+ Wild
+ Rain

The string form of a statement is as follows:

`<noun>[adjective_1:<temporal_statement_1_1,temporal_statement_1_n;adjective_2:<temporal_statement_2_1,temporal_statement_2_n]`

For example, let's take the following 4 narratives:
+ Sunny in the morning and overcast in the afternoon.
+ Moderate winds in the morning and gale force in the afternoon.
+ A mere sprinkling of rain drops in the early evening
+ The temperature was mild both during the day and night.

In the string form, this is codified as follows:

```shell
"sky[sunny:morning;overcast:afternoon]"
"wind[moderate:morning;gale_force:afternoon,evening,over_night]"
"rain[drops:early_evening]"
"temperature[mild:day,night]"
```

In CLI form, we add this narrative as follows:

```shell
poetry run climate add-narrative --locale "Palazzo Bronzino" --date 2023-09-14 -t "sky[sunny:morning;overcast:afternoon]" -t "wind[moderate:morning;gale_force:afternoon,evening,over_night]" -t "rain[drops:early_evening]" -t "temperature[mild:day,night]"
```