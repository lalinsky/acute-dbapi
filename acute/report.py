import glob

class OrderedDict(dict):
    'A simplistic OrderedDict implementation.'
    def __init__(self):
        self._keylist = []

    def __setitem__(self, key, value):
        if not self.has_key(key):
            self._keylist.append(key)
        dict.__setitem__(self, key, value)

    def keys(self):
        return self._keylist

    def items(self):
        return [(key, self.get(key)) for key in self._keylist]

    def __str__(self):
        xx = ["%s: %s" % (repr(key), repr(value)) for (key, value) in self.items()]
        rr = '{'+ ', '.join(xx) +'}'
        return rr


def dump_testcase_reports():
    qualfiles = glob.glob("reports/*")
    files = [qualfile[qualfile.find('/')+1:] for qualfile in qualfiles]
    print '|| Test Name ||','||'.join(files),'||'

    tests = OrderedDict()
    for qualfile in qualfiles:
 
      # Add each test to "tests" dict
      for test_result in open(qualfile, 'r').readlines():
          break_loc = test_result.find('...')
          test, result = None, None

          test = test_result[:break_loc - 1]
          result = test_result[break_loc + 4:-1]

          if (not break_loc) or test.startswith('----') or test.startswith('Ran '):
              continue

          if result == "ok":
              result = "Pass"
          if result == "(Unsupported) ok":
              result = "Fail"
          if result == "(Skipped) ok":
              result = "N/A"

          # Append this test result to list of all results for this test
          results = tests.get(test, [])
          results.append(result)
          tests[test] = results
  
          ##print '||', test, '||', result

    for (key, value) in tests.items():
        if key.strip()=='O' or value == ['N/A', 'N/A', 'N/A']:
            continue
        print '||', key, '||', ' || '.join(value), '||'


def dump_supported_features():
    import drivers
    features = OrderedDict()
    for nbr, driver_features in enumerate([drivers.DriverBase, drivers.pysqlite2, 
               drivers.MySQLdb, drivers.psycopg2, drivers.ibm_db]):
        for feature in dir(driver_features):
            if (feature[:1] == '_' or 
                hasattr(getattr(driver_features, feature), '__call__')):
                continue   # Skip private attributes & methods

            value = getattr(driver_features, feature)
            (doc, supports) = features.get(feature, ['', []])
            if not doc:
               doc_attr = '_' + feature + '__doc__'
               doc = getattr(driver_features, doc_attr)
            supports.append(value)

            features[feature] = (doc, supports)

    #Output the summary & introduction section
    print """#summary Comparison of core features provided by several DB-API implementations. \
Covers features that are universal to all DB-API implementations; features that are specific \
to a particular driver are not covered. \

= Introduction =
Comparison of core features provided by several DB-API implementations.  \
Covers features that are universal to all DB-API implementations ; features that are specific \
to a particular driver are not covered. 
    """
    #Output the table headers
    print "|| Feature || Feature Description || Default Value || pysqlite2 || MySQLdb || psycopg2 ||"

    #Output the table details
    for (feature, (doc, supports)) in features.items():
        print '||', feature, ' || ', doc, ' || ',
        for support in supports:
            print support, ' ||',
        print

if __name__ == '__main__':
    dump_testcase_reports()
    dump_supported_features()

