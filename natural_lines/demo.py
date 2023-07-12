import math
import random

from .draw import rect, cubic_bezier, arc

def demo(ctx, width, height):
    a = 10
    w = 100
    ws = w * .9
    print_points = False
    random.seed()
    ctx.set_source_rgba(0, 0, 0, 1)
    rect(ctx, a, a, ws, ws, squiggle_strength=1, print_points=print_points)
    rect(ctx, a + w, a, ws, ws, squiggle_strength=2, print_points=print_points)
    rect(ctx, a + 2*w, a, ws, ws, squiggle_strength=5, print_points=print_points)
    rect(ctx, a + 3*w, a, ws, ws, squiggle_strength=7, print_points=print_points)
    rect(ctx, a + 4*w, a, ws, ws, squiggle_strength=10, print_points=print_points)
    ctx.stroke()

    ctx.set_source_rgba(0, 1, 0, 1)
    arc(ctx, a + 2*w + w/2, 150, 30, 30 * math.pi/180., 240 * math.pi/180., squiggle_strength=1, segments=5, n=10)
    ctx.set_source_rgba(0, 0, 1, 1)
    arc(ctx, a + 3*w + w/2, 150, 30, 280 * math.pi/180., 300 * math.pi/180., squiggle_strength=1, segments=5, n=5)
    ctx.set_source_rgba(1, 0, 0, 1)
    arc(ctx, a + 4*w + w/2, 150, 40, 0, 2.*math.pi, squiggle_strength=1, segments=48, n=1)

    ctx.set_source_rgba(0, 0, 0, 1)
    cubic_bezier(ctx, 10,170, 40,60, 120,180, 200,140, squiggle_strength=1, n=40)

    ctx.set_source_rgba(0, 0, 0, 1)
