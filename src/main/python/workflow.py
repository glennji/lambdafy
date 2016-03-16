submit_stages = {}


def stage(stage):
    def _stage_decorator(func):
        submit_stages[stage] = func

        def _call_stage(*args, **kwargs):
            return func(*args, **kwargs)

        return _call_stage

    return _stage_decorator


def submit(stage, *args, **kwargs):
    print "submitting for stage {}".format(stage)
    try:
        submit_stages[stage](*args, **kwargs)
    except ValueError:
        print "No stage implementation labelled '{}'".format(stage)


def finish(self, stage, changes):
    print "Finished {}, {} changes".format(stage, "with" if changes else "no")


def fail(self, stage, err):
    print "Failed {}: {}".format(stage, err)
