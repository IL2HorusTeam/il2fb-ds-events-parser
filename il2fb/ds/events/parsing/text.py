
def strip_spaces(string: str) -> str:
  # Works faster than split-join or regex. Results of 'timeit':
  #  - replace():               0.164354042999548
  #  - "".join(string.split()): 0.200693268001487
  #  - regex.sub("", string):   0.742091242000242  (regex = re.compile("\s+"))
  return string.replace(" ", "")
