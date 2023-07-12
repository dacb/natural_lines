import cairo

def render_png(filename='demo.png', width=512, height=512, draw_func=None, bg_rgba=(1, 1, 1, 1)):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    
    context = cairo.Context(surface)
    
    # paint background
    context.set_source_rgba(*bg_rgba)
    context.rectangle(0, 0, width, height)
    context.fill()

    if draw_func is not None:
        draw_func(context, width, height)
   
    surface.write_to_png(filename)
