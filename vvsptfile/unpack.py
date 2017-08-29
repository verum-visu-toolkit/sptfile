import struct
from re import compile as re_compile
from numpy import array as np_array

import format

first_numbers = re_compile('^\d+')


def unpack(sptfile_data):
    """
    Unpack and parse SPT binary file data

    Args:
        sptfile_data: input binary data (str)

    Returns:
        Parsed SPT (dict)
    """
    _, body, config = _unpack_raw_sptfile(sptfile_data)

    for name in ['num_channels', 'num_spectra', 'num_freqs']:
        config[name] = int(config[name])

    config['peak'] = float(config['peak'])

    channels = _structure_flat_channels_data(body=body, config=config)
    spt = create_spt(spectra_channels=channels, config=config)
    return spt


def _unpack_raw_sptfile(sptfile_data):
    """
    Unpack an SPT file's binary contents

    Args:
        sptfile_data: input binary data (str)

    Returns:
        Data (tuple)
    """

    header_fmt_str_block_len = int(first_numbers.match(sptfile_data).group(0))
    header_fmt_str = sptfile_data[:header_fmt_str_block_len].strip()
    header = struct.unpack_from(header_fmt_str, sptfile_data)
    config_vals = header[header_fmt_str_block_len + 3:]  # SPT is 3 chars long

    config = {
        config_name: config_vals[i] if i < len(config_vals) else None
        for i, config_name in enumerate(format.CONFIG_NAMES)
    }

    body_fmt_str = format.get_body_fmt_str(config)
    header_block_len = struct.calcsize(header_fmt_str)
    body = struct.unpack_from(body_fmt_str, sptfile_data,
                              offset=header_block_len)

    return header, body, config


def _structure_flat_channels_data(body=None, config=None):

    channels = []
    num_channels = config['num_channels']
    num_spectra = config['num_spectra']
    num_freqs = config['num_freqs']
    channel_len = num_spectra * num_freqs

    for channel_num in range(num_channels):

        channel_start_pos = 8 + channel_num * (channel_len + 8)
        channel_end_pos = channel_start_pos + channel_len
        flat_channel = body[channel_start_pos:channel_end_pos]

        spectra = []
        for spectrum_num in range(num_spectra):
            spectrum_start_pos = spectrum_num * num_freqs
            spectrum_end_pos = spectrum_start_pos + num_freqs
            flat_spectrum = flat_channel[spectrum_start_pos:spectrum_end_pos]

            spectrum = np_array(flat_spectrum)
            spectra.append(spectrum)

        channels.append(spectra)

    return channels


def create_spt(spectra_channels=None, config=None):
    # Write channel spectra data
    channels = {}
    for channel_num, spectra in enumerate(spectra_channels):
        channel_as_list = []

        # pbar.start('Channel {:d}'.format(channel_num))

        num_spectra = len(spectra)
        for num_spectrum, spectrum in enumerate(spectra):
            channel_as_list.append(spectrum.tolist())

            # pbar.set_progress(num_spectrum, num_spectra - 1)

        channels['channel%d' % channel_num] = channel_as_list

        # pbar.end()

    file_data = {
        'data': channels,
        'config': config
    }
    return file_data
