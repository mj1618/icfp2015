#!/usr/bin/env python

RENDER_TOP_LEFT = u"╔═══" 
RENDER_TOP_MID = u"╦═══"
RENDER_TOP_RIGHT = u"╗\n"
RENDER_BODY_LEFTMID = u"║ {} "
RENDER_BODY_RIGHT = u"║\n"
RENDER_BODY_OFFSET = u"  "
RENDER_ODDJOIN_LEFT = u"╚═╦═"
RENDER_ODDJOIN_MID = u"╩═╦═"
RENDER_ODDJOIN_RIGHT = u"╩═╗\n"
RENDER_EVENJOIN_LEFT = u"╔═╩═"
RENDER_EVENJOIN_MID = u"╦═╩═"
RENDER_EVENJOIN_RIGHT = u"╦═╝\n"
RENDER_BOTTOM_LEFT = u"╚═══"
RENDER_BOTTOM_MID = u"╩═══"
RENDER_BOTTOM_RIGHT = u"╝\n"

RENDER_GRID_FILL = u"#"
RENDER_GRID_EMPTY = u" "

def render_grid(grid):
    assert len(grid) > 0
    assert len(grid[0]) > 0

    height = len(grid)
    width = len(grid[0])
    for row in grid:
        assert len(row) == width

    output = RENDER_TOP_LEFT + RENDER_TOP_MID*(width-1) + RENDER_TOP_RIGHT

    row_index = 0
    while row_index < height:
        
        if row_index % 2:
            output += RENDER_BODY_OFFSET
        for i in range(width):
            output += RENDER_BODY_LEFTMID.format(RENDER_GRID_FILL if grid[row_index][i] else RENDER_GRID_EMPTY)
        output += RENDER_BODY_RIGHT

        if row_index != height-1:
            if row_index % 2:
                output += RENDER_EVENJOIN_LEFT + RENDER_EVENJOIN_MID*(width-1) + RENDER_EVENJOIN_RIGHT
            else:
                output += RENDER_ODDJOIN_LEFT + RENDER_ODDJOIN_MID*(width-1) + RENDER_ODDJOIN_RIGHT
    
        row_index += 1

    if (height-1) % 2:
        output += RENDER_BODY_OFFSET
    output += RENDER_BOTTOM_LEFT + RENDER_BOTTOM_MID*(width-1) + RENDER_BOTTOM_RIGHT

    return output



