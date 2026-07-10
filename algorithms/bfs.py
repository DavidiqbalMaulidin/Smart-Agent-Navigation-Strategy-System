from collections import deque

def bfs(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    queue = deque([(start, [start])])
    visited = set()

    nodes_explored = 0

    directions = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1)    # right
    ]

    while queue:
        current, path = queue.popleft()

        if current in visited:
            continue

        visited.add(current)
        nodes_explored += 1

        if current == goal:
            return {
                "path": path,
                "nodes_explored": nodes_explored
            }

        for dr, dc in directions:
            nr = current[0] + dr
            nc = current[1] + dc

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] != 1 and
                (nr, nc) not in visited
            ):
                queue.append(
                    (
                        (nr, nc),
                        path + [(nr, nc)]
                    )
                )

    return {
        "path": [],
        "nodes_explored": nodes_explored
    }