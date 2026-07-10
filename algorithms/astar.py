import heapq


def heuristic(a, b):
    """
    Manhattan Distance
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}

    g_score = {start: 0}

    nodes_explored = 0

    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1)    # right
    ]

    while open_set:
        _, current = heapq.heappop(open_set)

        nodes_explored += 1

        if current == goal:

            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()

            return {
                "path": path,
                "nodes_explored": nodes_explored
            }

        for dr, dc in directions:

            nr = current[0] + dr
            nc = current[1] + dc

            neighbor = (nr, nc)

            if not (
                0 <= nr < rows and
                0 <= nc < cols
            ):
                continue

            if grid[nr][nc] == 1:
                continue

            tentative_g = g_score[current] + 1

            if (
                neighbor not in g_score or
                tentative_g < g_score[neighbor]
            ):

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score = (
                    tentative_g +
                    heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_set,
                    (f_score, neighbor)
                )

    return {
        "path": [],
        "nodes_explored": nodes_explored
    }