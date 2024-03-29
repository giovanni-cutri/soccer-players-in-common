# soccer-players-in-common
 
As a soccer fan, have you ever looked at two or more teams and wondered if any footballers played for all of them? 

Thanks to this Python script, which scrapes data from *[worldfootball.net](https://www.worldfootball.net/)*, you can find an answer!

## Dependencies

All the necessary libraries are listed in the *requirements.txt* file.

You can install them by running:

```
pip install -r requirements.txt
```

## Usage

Run *soccer-players-in-common.py* and follow the instructions printed on the screen: type the number of teams you are interested in and then the names of said teams, **as they are reported on *worldfootball.net***.

You will get a list containing the names of the players.

You can also filter results by the country or position of the players, using the following command-line arguments:

````
-c, --country       the country of the players
-p, --position      the position of the players
````

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/soccer-players-in-common/blob/main/LICENSE) file for details.
