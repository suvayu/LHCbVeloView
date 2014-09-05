def run_view_resolver(name):
    """Resolve a job for the run view.

    Requires the job name to start with `run_view`.
    """
    valid_names = [
        'pedestals',
        'common_mode',
        'noise',
        'clusters',
        'hv_current',
        'cluster_mpv',
        'cluster_fwhm',
        'cluster_size',
        'occupancy'
    ]
    module, method = name.split('.')
    if module != 'run_view' or method not in valid_names:
        return None
    return 'veloview.{0}'.format(name)
