from .. import utils
import struct
import format


def pack(spectra_channels=None, config=None):
    pbar = utils.pbar
    pbar.start('Generating an SPT file', show_header=True)

    fmt_str_block = list(format.SPT_FILE_FMT_STR_BLOCK)
    name_str = list('SPT')
    # num channels, num spectra per channel, num freqs per spectrum, read rate
    config_block = [config['num_channels'], config['num_spectra'],
                    config['num_freqs'], config['speed']]

    encoded_channel_data = []
    for channel_num, spectra in enumerate(spectra_channels):

        pbar.start('Channel {:d}'.format(channel_num))

        encoded_channel_data += list('channel%d' % channel_num)

        num_spectra = len(spectra)
        for num_spectrum, spectrum in enumerate(spectra):
            values = spectrum.tolist()
            for value in values:
                encoded_channel_data.append(value)

            pbar.set_progress(num_spectrum, num_spectra - 1)

        pbar.end()

    body_fmt_str = format.get_body_fmt_str(config)
    full_fmt_str = format.HEADER_FMT_STR + body_fmt_str

    file_data = fmt_str_block + name_str + config_block + encoded_channel_data

    file_data_packed = struct.pack(full_fmt_str, *file_data)

    pbar.end(show_header=True)

    return file_data_packed

