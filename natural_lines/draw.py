import math
import random

import numpy as np


def quad_to(ctx, x1, y1, x2, y2):
    x0, y0 = ctx.get_current_point()

    c1x = (x0 + 2.*x1) / 3.
    c1y = (y0 + 2.*y1) / 3.
    c2x = (x2 + 2.*x1) / 3.
    c2y = (y2 + 2.*y1) / 3.

    ctx.curve_to(c1x, c1y, c2x, c2y, x2, y2)

def time_to_point(sx, sy, fx, fy, t):
    # scale the time value, which should be between 0 and 2, to 0 and 1
    tau = t / 2.0
    poly_term = 15. * math.pow(tau, 4.) \
              - 6. * math.pow(tau, 5.) \
              - 10. * math.pow(tau, 3.)

    return {"x": sx + (sx - fx) * poly_term,
            "y": sy + (sy - fy) * poly_term }

def get_squiggle(prev, current, strength=5., seed=None):
    # find the midpoint
    midpoint = {"x": (prev["x"] + current["x"]) / 2., \
                      "y": (prev["y"] + current["y"]) / 2.};

    # displace by a random value between -5 and 5
    # the paper calls to do this w.r.t. the normal of the line
    # but we'll just do it on the circle.
    if seed is not None:
        random.seed(seed)
    def rng():
        return random.random()

    range_adjust = strength / 2.
    displacementX = rng() * strength - range_adjust;
    displacementY = rng() * strength - range_adjust;

    midpoint["x"] += displacementX;
    midpoint["y"] += displacementY;

    #print(f"{midpoint['x']}, {midpoint['y']}")

    return midpoint;

def line(ctx, sx, sy, fx, fy, squiggle_strength=10., seed=None, print_points=False, dt=None):

    if dt is None:
        dist = math.sqrt(math.pow(sx - fx, 2) + math.pow(sy - fy, 2));
        # these are the results of a small number of asthetic tests and may
        # evolve or become arguments
        if dist < 100:
            dt = 0.8
        elif dist < 200:
            dt = 0.5
        elif dist < 400:
            dt = 0.3
        else:
            dt = 0.2

    last_point = {"x": sx, "y": sy}
    ctx.new_path()
    ctx.move_to(last_point["x"], last_point["y"])

    #print(f"last.x = {last_point['x']}, last.y = {last_point['y']}")
    for t in np.linspace(0, 2., int(2. / dt) + 1):
        current_point = time_to_point(sx, sy, fx, fy, t)
        squiggle_control_point = get_squiggle(last_point, current_point, strength=squiggle_strength, seed=seed)
        quad_to(ctx, squiggle_control_point["x"], squiggle_control_point["y"], current_point["x"], current_point["y"])

        if print_points:
            print(f"current.x = {current_point['x']}, current.y = {current_point['y']}")
            print(f"squiggle.x = {squiggle_control_point['x']}, squiggle.y = {squiggle_control_point['y']}")

        last_point = current_point;

    ctx.stroke()

def rect(ctx, x, y, w, h, squiggle_strength=5., seed=None, print_points=False):
    line(ctx, x,     y    , x + w, y    , squiggle_strength=squiggle_strength, seed=seed, print_points=print_points)
    line(ctx, x + w, y    , x + w, y + h, squiggle_strength=squiggle_strength, seed=seed, print_points=print_points)
    line(ctx, x + w, y + h, x    , y + h, squiggle_strength=squiggle_strength, seed=seed, print_points=print_points)
    line(ctx, x    , y + h, x    , y    , squiggle_strength=squiggle_strength, seed=seed, print_points=print_points)

def arc_segment(ctx, xc, yc, radius, angle1, angle2, n=50, squiggle_strength=1):
    while angle2 < angle1:
        angle2 += 2. * math.pi

    # find x1 and x4 - the start and end points on the arc
    x1 = xc + radius * math.sin(angle1)
    y1 = yc + radius * math.cos(angle1)
    x4 = xc + radius * math.sin(angle2)
    y4 = yc + radius * math.cos(angle2)

    # https://stackoverflow.com/posts/44829356/revisions
    ax = x1 - xc
    ay = y1 - yc
    bx = x4 - xc
    by = y4 - yc
    q1 = ax * ax + ay * ay
    q2 = q1 + ax * bx + ay * by
    k2 = 4. / 3. * (math.sqrt(2 * q1 * q2) - q2) / (ax * by - ay * bx)
    x2 = xc + ax - k2 * ay
    y2 = yc + ay + k2 * ax
    x3 = xc + bx + k2 * by
    y3 = yc + by - k2 * bx
    cubic_bezier(ctx, x1, y1, x2, y2, x3, y3, x4, y4, n=n)

def arc(ctx, xc, yc, radius, angle1, angle2, segments=10, n=10, squiggle_strength=1):
    while angle2 < angle1:
        angle2 += 2. * math.pi

    last_angle = angle1
    for current_angle in np.linspace(angle1, angle2, segments)[1:]:
        arc_segment(ctx, xc, yc, radius, last_angle, current_angle, n=n, squiggle_strength=squiggle_strength)
        last_angle = current_angle


# from rosetta code
def cubic_bezier(ctx, x0, y0, x1, y1, x2, y2, x3, y3, n=40, squiggle_strength=1):
    ctx.new_path()
    ctx.move_to(x0, y0)

    pts = []
    for i in range(n+1):
        t = i / n
        a = (1. - t)**3
        b = 3. * t * (1. - t)**2
        c = 3.0 * t**2 * (1.0 - t)
        d = t**3

        x = int(a * x0 + b * x1 + c * x2 + d * x3)
        y = int(a * y0 + b * y1 + c * y2 + d * y3)
        pts.append((x, y))

    for i in range(n):
        line(ctx, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], squiggle_strength=squiggle_strength)

    ctx.stroke()
