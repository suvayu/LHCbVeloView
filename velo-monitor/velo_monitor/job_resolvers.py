def run_view_resolver(name):
    """Resolve a job for the run view.

    Requires the job name to start with `run_view`.
    """
    module, method = name.split('.')
    if module != 'run_view' or method != 'get_plot':
        return None
    return 'veloview.{0}'.format(name)
