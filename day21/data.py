example = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........

""".strip()

data = """
...................................................................................................................................
..#......##................#......#.#............#.....#....#.................#.......#.....#.#.....##.....#.#........#.#..#....#..
.......#....###...###.........##...#.#..#.....#......#...#................................................#.........##.#.#..#..###.
....#.....#..#.#.....#....#.#.##.#..........#...#.......................#...##......#...#.#.#....###.....#....#......#....#...#.#..
..##.#......##...##......#...#.#.#..##.#......#.........#............................#.........#...................#....#........#.
.#..........#....#.....#.....#..#.....#........#...........................#..#.#........#....#.#.....#.#...#..................#...
.#.#.#.#.#............#.....#.....#....#...........#.........................................#...#.......#....#....#.......#..#..#.
.#......##.#.#..............#....#.....####....#..#.............................#............#..............###.#.....#............
..#........#.........#....#................##..................#..#........................#.#.#.......###..#...#...#..............
.......#........#.......##.#..#.............................#.........................#........#........#.#.#..##..#..#.#......#...
.....#.#.#.##....................#.#.#....##.#....#...............#..###.......#.............#......#....#...#..#...............#..
.#..#...#.........#............#..#......#.#.....#...........#....#.....#..........#...........##......##.....#.#........#.........
........#.....#..#......#....#.#........##.#...........................#.......................##.....##..#........#.#......#.#....
..........#..#...............#..#..........#...#..........#.....#..#...#...........#..................#...................###..#.#.
.#..#......#..#...#.#..#.....#.....###.........#...........#.#............#........#.....###.......##.....#.#.#...........#........
.#.....#....##..##..#...........#.....#.......#.........#...#..............##..........#...#..#..#...#............#.#.#.......#....
.#..#.#.#.......#....................#................#.#................#..............#..#..##..#.#..#..###....#.....#..#........
...#.....#.......##..#............##.....#..#..........#......##.......#..............#.#..#.......#.........#.....................
..#.#.....#.......#....#.........##................##....#...#.......................................#.......#.#..##......#...#....
...........#.#.#.....#...#.#..#....#..#..............#.#.#....#....##...................#....#......#........#....#..##...#...#....
....#........#....#.#..##...##...................#.....#........#....#...#.#.#.#.............#.....#.#.......##..#.#.......#....#..
.##.#....#.......#.#......##.....#.#.#............#.......#........#...........................#.......##...#...##....#.........#..
.......#....#................#..##.............###.....#.............#....#......##........#.##...................#................
....#.......##.................#...................##..#..............#.......##..##...........#..##...#.#.....#...###.....#.......
.#.............................##................#......#...#...........#.#.#......#...........##.....##................#.#........
.#.##.#........##.........#.....##.#...........#...........#.#....##.....##.......#...........#..#.......#.##......#.....#...#...#.
...#...##.......#.#...#.......#...#.................#......#..#...............#.#.#........................#...........#.....#.....
.......#.#...#..##.........#.....#........#..##.#.#....#........#..##..........#...#..#..............#......##..#....#.......#.....
...##.......#..#......#...........................#..#.........#.............##........#.........#...#................#..###.......
.........................##................#.#...##....#......#.#..#....#....#....#..#..........................#.#..#.......#.....
....#.....#...#.........#..#............##...#..#........#........##.#..#...........#..........................#...#.....#......#..
.......................#..............#..#...#...............#..#.#..#..#...#...#.#..........................#.......#..#..........
....##.#.............#...#.................##....#......#....#.##........#...............##............##.#.................#...#..
...#...#..#...........#........................#....#.#.......#..........#.......##.......................##..#.#....#...........#.
..............#......##............#...##.#..........#....#....#.......#...................##..............#...#........#..#..#....
.......#............##..#.#........#....#.##....#.....#.#.#.....#......#....#..........#...#...#..................#....##..........
.............#....#...#..#..............#.......#........##...#...#..#....#...........##....#............#....#...#.#.#........#...
.#.....###.#.....................#..........#.#.....#..#...#.#.#.....................#.............................................
.#...#...........#.....#...........#....#....##.........#..#......#..#....#.....#....#.#...#..................##.........#..#....#.
.#.......#......................##.........................#....#...#......##......#........#......#.........#.......##.#...#......
....##...........#...#.......#.......##........#................#.......#.#.##.............#..#.#................##.....#..#...##..
..........#.#.................#..#..#...##.###.......##.#..#........##......##..##...#...#..#..#####.#.........#..#...#.#..........
..#....#..#.#...............#...............#.#..####......#..........##.#...##...#.#................#................#.##..##..#..
..........#....##..........#..............#.......#.......#.#...#..##.....................#.#.#....#...#...........#...............
...#.......#.................#...........#..#........#...#..............#..............#....#...##....................#...#........
...####...#.............##.....#............#.##.....#...#..#.#......#.............#.........##....##...................#.#...#....
....#.....#.............#.....##...#..#...........#..#.....#......#.#.....#......#.....#....#......#...............................
.....#...#..##.............#....##...#.......#...##......##.....#.......#...#........................#.#.......................#.#.
.###.....#...#................#....#.....................###.#....#..#.#....................#....................................#.
...#..................#..#..#........##....#..#.#.##..#.#...#.........#..#.#...#...............#...........##..........##.#........
...........#..................#.............#...#.#.#......###..........#...#.......#.......#....#........#.#...........##.........
.......#..#.......##..#............................##.....#.#..#.......##.....#...#.......#...........#....#...#...................
...#.............#.................#.#.###......##.........####.....#..##.............#.......##.....#....................#........
.#................#.#..#..#..#..##.....#.......#..#.....#.......#....#.......#.............#.##......#.#.....#..............#..#...
.....#.................#...#....#.#...#.#......#.#...........#............#...#..........................###...#.................#.
...........................#..#.#..#...#...............#...#...#....#...........##...........#...#..#.#........#..###........#.....
..................##....##......##.#........#..#...........#......#..............#........#...#..............#...#.#..........##...
...#...............#...###..#...........#.....#.......##.#...#..........##.....#........#.#.#..................##..#............#..
..#........#......#.....#.........#.......##......#..........#...........#..#.##....#...................#.##.......##..........##..
...............#...##....###.........#...#..............#.#.......#...#.....#.........##..#.......##..............#................
............#........#......##.#................##...#.....##...#.....##.......#..................#........#.##.#.....#.##.........
..........#....#....#...##..#.#..........#.............##..#......#.#......#.#..............#........#...#..#............##........
...........#.......##...#......#..#......#.#.......#.........#...........#.....#..##...#...##..............##........#.#..#........
............#....#.......#..........#..##..#...##...#.#.#.....#............#.#.......#.#..#........##......#....#.#.....#..........
.......................#...........##.#..........#.....#.#.#..........#.#.............................#....##.....##......#..#.....
.................................................................S.................................................................
.....#.##.#..........#..#..#........#.#...#......#......#....#.#.....#.#..............................#.............#.....#........
......#.....#....#..#........#.....#.........#........#..#...#.......#.#.....##.....##....#..#.#..#.#..........#....#...#..........
...................##....#........#.#.........#.......#........................#.....#.#...#..###.......###..#...#.....##..........
.........#.#...#.#.#.#......#............#....#.#........................#.......#.#.#........#..............#..#.#...#............
...............#..#.#...#..#......#....#....#.......##...............#.#.#..#......#...##.........................#................
.#.....................#..#..#..............#....#...#...#....##....#.#...#.......##.#...........###...#.......#####...............
..#........#............#.#...#.......#...#...........#......#....#...........#..#..............#....#..#...##.......#..........##.
.#.#.....................#..............#.#.........#.#...............#......#......#.#..##...#......#......#........##............
..............#....#.#....##.##.....#........#...............#..........................#...#....#.##.........#....................
..................##...............##..#....##..............#.....#...#........#.#...#...............###....#................#.###.
.#...#............#.#.#..##....#......#........#.#........#.....#......#.......##.....#.#.#.....................#..................
...#.#.............#.............#.#.##...#.#.............................................#....##..#.#.....#..................#....
......#............#...#.......#.#..#......#.......#.....#.#.......#...##....##....##.............####...................#..#......
.........#........#.....#..#...........#.#.......##.#..#....#..#.....#.#..#.#....#......#...................#.............#....#.#.
......#................#..................#............#.............#.....#.........#...##.....#.#.##..#..###.........##.......#..
.............................#....#.....#.#............##....#..#......#..#.#....#.................#....#...#.........#............
....#.#.....................#........#.........##..............#...#..............................#....#.................#.......#.
.#..#.................#..........#..#....#........##..#...............#......####.....#....#.....#..#....###........#.#.........#..
....##........#.........#...#..##.#.##....#......##........#......###..........#.#...#....#..#......................#........##....
........#.....#.#.........#......#.#........#....#..##....##................##.......#...#........#...........................#....
.#...........#............#..........#.......#.##.......#.#........#...#..###...#..#......#.............#................##....##..
..................#..........##...##....##.#.....#.....####........##........#...#.........#...#.....#..#...........##......#..#.#.
...............#.....................#................#...#....#......................#.#.......#...............#.....#......#...#.
...#............#.............#.##...................#....#...#.....#...#...........#.#...#........#................##.....#.......
...........#........#..................#.#..#.#.....#...............#.....#.#........##.......#..#.#..........#.............#......
..#.....#....#.#.................#.#.........#.......##.....#.........#.....#...............#.#...##.......................#....#..
......###....#....#.#..#....................#....#....#..#........#...#.#...##........#..##........#............#.........#....#.#.
...#.#.....#....#......#.........#..##...#.##...#....#..##..#.#........#..##.#.................#...................................
.........###.#...#...#...........................#.........#.#.##....#.#...#..........#..#.......#.........##.....#......#...#.#...
.................#.....#..........#.#..#..###..................#........##....#.........#...................#....#.........#.....#.
.#..#....#..#...#.....#............#.#..........#....#.#..#..##......................#..#..#......................#.............#..
..#..#.#...#..#.....#...............................#.........##......#.............#.##...............#..#.##.......##..#.......#.
.....#...#.#....#...#..#..............#......#.#................#....#..#...........#.....#.#................#.##.........##.......
....#......##.........#.#...#.........#......#.##...##........#....#.................#......................###......#.....##......
...#.#.....#.....#.#.#.#...............#..#.....#.#...............#.#.........##.....##..#...................#.......#.#...........
..#.....#..#.....#...##....##..##.........#...#....#....#...#......##.##..#..#.........#............#..#.##...................#....
...#....###...#..........##......#........#..........#.............###.....#.....#..#.#...............#...##....#...##..#..#...#.#.
...#................#.........#................#..#..#..#.#...............#.....#...................#.................#...#........
.#.......#.#.#.#.......#...................#...#......##.....#........##.....#...#........................#..#..#....#......#..#...
..##..#....#...#.......#........#...#....................###........##............#...............#....#.......#............#......
.#............#.....#...##....#.......................#..#....#........#..........#..#...........#..#........................#.....
..........###....#..#.#..#..#.........#.......#...#......#....#...#.............#............#.....................#.#...#.......#.
...#..#..............................#.........#........##....##....##..##.....##......................#........#.....#...#...#.#..
.#.#.................##.......#.#.#.....................#.....#........#......##.............#.......#..##....##........#.#.#......
...##.#.#..#...#........#......#.....#....................#........#.#.....#...#................#........#...#.##.....#..#.......#.
.##.#.......#..#....#..#....#......#.....................#...........#......#.#..............#...#......#.#.......#......#.#.......
....#................###...#.......#...#..##........#...................#.......................#..##.......#................###...
.........##.....#.....##..........#....#..##.............#.....##......##....#..................#..##.................#...#........
.#..#....#....#.#........#..#................#............#.......#........#...................................##........#.......#.
.........##...#........#.#............#.......#..........#.................#..........................#......##.....#....#.#....##.
...##......................#.....#....#.##...................#.............#..............#....#......#.............#........#.....
....#...........##.......#...#.....#.......#..#................#........##......................#..#....#..##.....#.#..............
......#..#...#......#.......#.....#.#..........#................#................#.....#.#.#....#...#..............................
....#....#..#...##..##.......#...................##..............................#........#................#....#..........#..#.#..
....#...##.....##...#......#.............#.......#..............................#..........#...............................#.#.....
.##.#.....#..#.......#..##................#..#..##..#..........#..............#..#.#....#.#..#..##.#....#.##..#............#.....#.
....#..#.#............##.....##.............###.#............#.#.....#....................#.#........#....#.#..#..#...........#.#..
.#.......#..................#...................#....#..........#...........#....#......#.........#.............##...............#.
..#...............##..#.#...###.....#...#....#....#...#........#..#....................##.#.......#...#.......#................#...
..#.##..........##......#...#.#.#.#.....##.....#.##..#..#.........#........#....................#.................#............##..
....#...##.......##....##...#.#..............#.....#......................#.#......#...................#..#.#...##.#..........#..#.
.#.#....#..##..#..............###.......................###................#..#..#..##....#....#............##..#..................
......#..#......#.........#.#.#...#.......................##..............##...#.....##.#....#......#....#.........#.......#.....#.
....#.........#...............#...#............#.........#................##.#..........#.............#.......................#.##.
...................................................................................................................................

""".strip()

