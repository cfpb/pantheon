from appring import apps

def gen_context(request, tile_names, context, tile_contexts):
    """
    :param request request: Djange request object
    :param iterator tile_names: tuple of "app.function" tile name
    :param context context: context
    :param iterator tile_contexts: pointer into context to a list
        where tile contexts will be inserted
    :returns str: returns rendered html
    """
    for tile_name in tile_names:
        app_label, tile_label = tile_name.split('.')
        app = getattr(apps, app_label)
        tile = getattr(app.tiles, tile_label)
        tile_contexts.append(tile(request, context))

    return context

