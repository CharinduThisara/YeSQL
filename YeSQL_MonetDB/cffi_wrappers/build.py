from cffi import FFI
import os

ffi = FFI()

ffi.embedding_api("""
typedef long long int64_t;

int cleancode_wrapped(char* input, int size, char** result);
int cancelledbool_wrapped(double* input, int size, uint8_t* result);
int divertedmap_wrapped(double* input1, char* input2, int size, char** result);
int fillInTimesUDF_wrapped(double* input1, char** input2, char** input3, int size, double* result);
int gettime_wrapped(int* input, int size, char** result);
int getcity_wrapped(char** input, int size, char** result);
int getstate_wrapped(char** input, int size, char** result);
int getcity_py_wrapped(char** input, int size, char** result);
int getstate_py_wrapped(char** input, int size, char** result);
int toint_wrapped(char** input, int size, int* result);
int defunctyear_wrapped(char** input, int size, int* result);
int getairlinename_wrapped(char** input, int size, char** result);
int getairlineyear_wrapped(char** input, int size, int* result);
int extractbd_wrapped(char** input, int size, int* result);
int extracttype_wrapped(char** input, int size, char** result);
int extractpcode_wrapped(char** input, int size, char** result);
int extractba_wrapped(char** input, int size, int* result);
int extractsqfeet_wrapped(char** input, int size, int* result);
int extractprice_sell_wrapped(char** input, int size, int* result);
int avg_word_len_wrapped(char** input, int size, double* result);
int extractpcodenew_wrapped(char** input, int size, char** result);
int sectohuman_wrapped(char** input, int size, char** result);
""")

ffi.set_source("libwrappedudfs", "#include <stdint.h>", libraries=[], extra_link_args=["-pthread"])

ffi.embedding_init_code(f"""
import struct
import sys, os
from importlib import reload
from libwrappedudfs import  lib, ffi
#curmodulepath = os.path.dirname( os.path.abspath('./') )
env1 = os.path.expanduser(os.path.expandvars('$PYTHONPATH'))
env2 = os.path.expanduser(os.path.expandvars('$FUNCTION_PATH'))

sys.path.insert(0, env2)
sys.path.insert(0, env1)
import flights
import zillow
import row.date as row_date
import aggregate.date as da

@ffi.def_extern()
def getairlinename_wrapped(input,insize,result):
  reload(flights)
  for i in range(insize):
    result[i] = ffi.new("char[]", flights.getairlinename(ffi.string(input[i])).encode("utf-8"))
    # result[i] = lib.strdup(ffi.from_buffer(buffer(flights.getairlinename(ffi.string(input[i])))))
  return 1

@ffi.def_extern()
def getcity_wrapped(input, insize, result):
  # importlib.reload(mymodule)
  reload(flights)
  for i in range(insize):
      result[i] = ffi.new("char[]", flights.getcity(ffi.string(input[i])).encode("utf-8"))
      # result[i] = flights.getcity(lib.strdup(input[i]))
  return 1

@ffi.def_extern()
def getstate_wrapped(input, insize, result):
  # importlib.reload(mymodule)
  reload(flights)
  for i in range(insize):
      result[i] = flights.getstate(input[i])
  return 1

@ffi.def_extern()
def getcity_py_wrapped(input, insize, result):
  reload(flights)
  tmpstrs = [flights.getcity_py(ffi.string(input[i])) for i in range(insize)]
  for i in range(insize):
      result[i] = ffi.from_buffer(buffer(tmpstrs[i]))
  return 1

@ffi.def_extern()
def getstate_py_wrapped(input, insize, result):
  reload(flights)
  tmpstrs = [flights.getstate_py(ffi.string(input[i])) for i in range(insize)]
  for i in range(insize):
      result[i] = ffi.from_buffer(buffer(tmpstrs[i]))
  return 1

@ffi.def_extern()
def toint_wrapped(input,count,result):
  for i in range(count):
      result[i] = flights.toint(ffi.string(input[i]))
  return 1


@ffi.def_extern()
def getairlineyear_wrapped(input,insize,result):
  reload(flights)
  for i in range(insize):
        result[i] = flights.getairlineyear(ffi.string(input[i]))
  return 1

@ffi.def_extern()
def defunctyear_wrapped(input,insize,result):
  reload(flights)
  for i in range(insize):
      py_inp = ffi.string(intput[i]).decode("utf-8")
      result[i] = flights.defunctyear(ffi.string(py_inp))
  return 1

@ffi.def_extern()
def gettime_wrapped(input,insize,result):
  reload(flights)
  tmpstrs = [flights.gettime(input[i]) for i in range(insize)]
  for i in range(insize):
    result[i] = ffi.from_buffer(buffer(tmpstrs[i]))
  return 1

@ffi.def_extern()
def cleancode_wrapped(input,insize,result):
  reload(flights)
  for i in range(insize):
    result[i] = ffi.from_buffer(buffer(flights.cleanCode(input[i])))
  return 1

@ffi.def_extern()
def divertedmap_wrapped(input1, input2, insize, result):
  reload(flights)
  for i in range(insize):
    result[i] = ffi.from_buffer(buffer(flights.divertedmap(input1[i], input2[i])))
  return 1

@ffi.def_extern()
def cancelledbool_wrapped(input,insize,result):
  reload(flights)
  for i in range(insize):
    result[i] = flights.cancelledbool(input[i])
  return 1

@ffi.def_extern()
def fillInTimesUDF_wrapped(input1,input2,input3, insize,result):
  reload(flights)
  for i in range(insize):
      result[i] = flights.fillintimes(input1[i],ffi.string(input2[i]),ffi.string(input3[i]))
  return 1

@ffi.def_extern()
def extracttype_wrapped(input,insize,result):
  reload(zillow)
  for i in range(insize):
    result[i] = ffi.from_buffer(buffer(zillow.extracttype(ffi.string(input[i]))))
  return 1

@ffi.def_extern()
def extractpcode_wrapped(input, insize, result):
  from importlib import reload
  reload(zillow)
  for i in range(insize):
      s = zillow.extractpcode(ffi.string(input[i]))
      result[i] = ffi.new("char[]", s.encode("utf-8"))
  return 1
                        
@ffi.def_extern()
def extractpcodenew_wrapped(input, insize, result):
  from importlib import reload
  reload(zillow)
  for i in range(insize):
      s = zillow.extractpcodenew(ffi.string(input[i]))
      result[i] = ffi.new("char[]", s.encode("utf-8"))
  return 1

@ffi.def_extern()
def extractbd_wrapped(input,insize,result):
  reload(zillow)
  for i in range(insize):
    result[i] = zillow.extractbd(ffi.string(input[i]))
  return 1


@ffi.def_extern()
def extractba_wrapped(input,insize,result):
  reload(zillow)
  for i in range(insize):
    result[i] = zillow.extractba(ffi.string(input[i]))
  return 1

@ffi.def_extern()
def avg_word_len_wrapped(input,insize,result):
  for i in range(insize):
    words = ffi.string(input[i]).split()
    result[i] = sum(len(word) for word in words) / len(words)
  return 1


@ffi.def_extern()
def extractsqfeet_wrapped(input,insize,result):
  reload(zillow)
  for i in range(insize):
    result[i] = zillow.extractsqft(ffi.string(input[i]))
  return 1

@ffi.def_extern()
def extractprice_sell_wrapped(input,insize,result):
  reload(zillow)
  for i in range(insize):
    result[i] = zillow.extractprice_sell(ffi.string(input[i]))
  return 1

@ffi.def_extern()
def sectohuman_wrapped(input, insize, result):
    from importlib import reload
    reload(row_date)
    for i in range(insize):
      sec = ffi.cast("int64_t *", input)[i]
      human_readable = row_date.sectohuman(sec)
      result[i] = ffi.new("char[]", human_readable.encode("utf-8"))
    return 1
""")

output_dir = "YeSQL_MonetDB/cffi_wrappers"
os.makedirs(output_dir, exist_ok=True)
ffi.compile(tmpdir=output_dir, verbose=True)
