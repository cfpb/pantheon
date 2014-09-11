from appring import apps

def gen_service_context(request, context, action_names, service):
    pass

def gen_repo_context(request, context, action_names, model_contexts):
    """
    :param request request: Djange request object
    :param iterator action_names: tuple of "app_label.action_name" for which to display actions
    :param context context: context
    :param iterator model_contexts: pointer to the list of repo dicts, [{"model": repo_model}, ...], in the passed context
    :returns iterator: action info added to the model_contexts list

    call each action specified in action_names with each model specified in model_contexts
    and insert the returned data into model_contexts

    actions must be put in an actions.py folder in the root of the app. The action name is
    the app label and action callable label separated by a dot. Thus the action name 
    "users.enable_user" is the enable_user callable found in in the actions.py file inthe users app.

    A repo action must be a callable that accepts the request, the context, and a model
    and returns a dictionary containing:

        * name - 1-2 words suitable for a tab/button
        * title - descriptive title
        * description - 1-2 sentences describing action
        * cta - short call to action placed on button 
        * action - url to go to when cta clicked
        * method (default: GET) - POST or GET
        * form (optional) - form to display under description, before CTA
    """
    actions = []
    for action_name in action_names:
        app_label, action_label = action_name.split('.')
        app = getattr(apps, app_label)
        actions.append(getattr(app.actions, action_label))

    for model_context in model_contexts:
        model_context['actions'] = []
        for action in actions:
            model_context['actions'].append(action(request, context, model_context['model']))

    return model_contexts
