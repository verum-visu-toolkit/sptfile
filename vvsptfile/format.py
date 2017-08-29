"""SPT Binary file format"""

CONFIG_NAMES = ['num_channels', 'num_spectra', 'num_freqs', 'speed', 'peak']

# here, we encode the header with lengths and binary types; e.g. '4c' means a
#  block of 4 characters, representing the header (see python struct lib)
# this will also be written into the header of any spt file! this should
#  make it easy upon inspect to understand what the file is for, and make
#  it easy for any parser to read config for a SPT file.
#   for easy parsing of the format string, we will always match: (\d+\w)+)

# Best viewed at 16 bytes or 4 floats wide

# header format string: 16 characters
# SPT name: 3 characters ('SPT')
# padding: 5 empty bytes
# config: 4 floats (16 bytes)
#   1. number of channels
#   2. number of spectra (frames) per channel
#   3. num frequencies per spectrum
#   4. read rate
# padding: 8 empty bytes
HEADER_FMT_STR = '12c3cx{:d}f8x'.format(len(CONFIG_NAMES))
# the header will embed the string with fixed length
SPT_FILE_FMT_STR_BLOCK = HEADER_FMT_STR + ' ' * (12 - len(HEADER_FMT_STR))


def get_body_fmt_str(config=None):
    """
    create data format string when writing/ready file:
    for n channels:
      channeln header + padding: 16 characters ('channel0' + ' ' * 8)
      channeln data: length defined in write function (floats)
        length = num freqs * num spectra
      padding: 32 empty bytes
    """
    num_channels = int(config['num_channels'])
    num_spectra = int(config['num_spectra'])
    num_freqs = int(config['num_freqs'])
    return num_channels * ('8c{:d}f16x'.format(num_freqs * num_spectra))
