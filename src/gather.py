import datetime
import pickle


def getDataset():
    pickles = open('pickled.pic', 'r')
    repdataset = pickle.load(pickles)
    pickles.close()
    return repdataset


##- adorn the repdataset with parent/child relationships
def adorndataset(repdataset):
    children = (x for x in repdataset.items() if x[1]['fork'])
    for name, app in children:
        parentname = app['parent']
        parentapp = repdataset.setdefault(parentname,
          {'description': 'foster parent of %s' % name})
        app['parentapp'] = parentapp
        forkings = parentapp.setdefault('forkings', {})
        forkings[name] = app
        print 'added %s to %s, %s' % (name,
          parentname, parentapp['description'])


def freshpoints(pushed_at):
    """linear decline from 12*WEIGHT to no points at > 12 mo."""
    WEIGHT = 2
    if pushed_at is None:
        return 0
    now = datetime.datetime.utcnow()
    months_old = (pushed_at - now).days / 31
    fresh = 12 - months_old
    fresh = fresh > 0 and fresh or 0
    return fresh * WEIGHT


def score_item(app):
    """Just a sketch of a scoring system. Returns a dict of component scores.

    Ideally components are normalized right here, for complete decoupling,
    so they can be combined into a multicolored bar, whose total length is
    indicative of an app's usefulness.
    XXX: eye-of-beholder! may need different scores for different folks.
        Risk aversion, multilingual, need for massive scalability, etc.
    """

    score = {}
    score['forks'] = app.setdefault('forks',0)
    score['watchers'] = app.setdefault('watchers',0) / 10
    score['freshness'] = freshpoints(app.setdefault('pushed_at', None))
    return score


def depth_first_score(root):
    children = root.setdefault('children', {})
    upward = 0
    for app in children.values():
        upward += depth_first_score(app)
    score = score_item(root)
    score['upward'] = upward
    root['score'] = score
    return sum(score.values())


def score_dataset(repdataset):
    roots = (x for x in repdataset.items())
    for name, app in roots:
        depth_first_score(app)

def header():
    tup = ( 'name'.ljust(52),
            'tot'.rjust(5),
            'fks'.rjust(5),
            'wat'.rjust(5),
            'frs'.rjust(5),
            'upw'.rjust(5),
          )
    return ' ' + ''.join( tup )

def dataline(name, app):
    score = app['score']
    tup = (name.ljust(52,'.'), 
             str(sum(score.values())).rjust(5), 
             str(score['forks']).rjust(5), 
             str(score['watchers']).rjust(5), 
             str(score['freshness']).rjust(5),
             str(score.setdefault('upward', 0)).rjust(5) )
    return ''.join( tup )

def display_as_tree(myname, myapp, depth=0):
    print '  ' * depth, dataline(myname, myapp)
    children = myapp.setdefault('children', {})
    for name, app in children:
        display_as_tree(name, app, depth + 1)

def display_as_list(repdataset):
    print header()
    roots = (x for x in repdataset.items())
    for name, app in roots:
        display_as_tree(name, app)


if __name__ == '__main__':
    repdataset = getDataset()
    repdataset['marinho/hippocampus']['parent'] = 'redvasily/django-emailauth'
    print repdataset['marinho/hippocampus']
    adorndataset(repdataset)
    score_dataset(repdataset)
    display_as_list(repdataset)
