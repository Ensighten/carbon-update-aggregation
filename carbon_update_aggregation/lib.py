#!/usr/bin/env python

import os
import whisper


def get_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(".wsp"):
                abs_path = os.path.join(root, filename)
                relative_path = abs_path.split(root_dir)[1]
                yield relative_path


def filename_to_metrics_path(filename):
    # Remove leading '/'
    if filename.startswith('/'):
        filename = filename[1:]
    # Remove .wsp suffix
    filename = filename.replace('.wsp', '')
    # Change from carbon/blah/foo/baz to carbon.blah.foo.baz
    filename = filename.replace('/', '.')
    return filename


def get_full_file_path(root_dir, filename):
    # if the second argument to os.path.join starts with a slash, it won't include the first argument in the output
    if filename.startswith('/'):
        filename = filename[1:]
    return os.path.join(root_dir, filename)


def update_aggregations(filename, schemas, root_dir):
    metrics_path = filename_to_metrics_path(filename)
    changed = None

    for schema in schemas[:-1]:  # the last item is 'default', we don't want to bother changing anything to that
        if schema.matches(metrics_path):
            method = schema.archives[1]
            # TODO: check and set xFilesFactor?
            full_filename = get_full_file_path(root_dir, filename)
            old_method = whisper.setAggregationMethod(full_filename, method)
            if method != old_method:
                changed = {
                    'filename': 'full_filename',
                    'metrics_path': metrics_path,
                    'matched_schema_name': schema.name,
                    'old_aggregation_method': old_method,
                    'new_aggregation_method': method,
                }
                print "changed {} to {} ({}, was {})".format(metrics_path, method, schema.name, old_method)
            # rules are in priority order, so only apply the first
            break

    return changed


def update_storage_aggregations(storage_dir, conf_dir):
    # we have to set this before importing carbon.storage or else it will throw an uncaught exception, but we can
    # only do it once we've gotten conf_dir from the command-line options
    import carbon
    import carbon.conf
    carbon.conf.settings['CONF_DIR'] = conf_dir
    import carbon.storage

    schemas = carbon.storage.loadAggregationSchemas()
    root_dir = storage_dir

    # collect a list of changes files for the calling code to process (this is especially useful for eg. ansible)
    changes = []
    for filename in get_files(root_dir):
        change_details = update_aggregations(filename, schemas, root_dir)
        if change_details:
            changes.append(change_details)

    return changes
