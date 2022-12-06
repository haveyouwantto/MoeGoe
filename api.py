import soundfile as sf
from text import text_to_sequence
from models import SynthesizerTrn
import utils
import commons
from torch import no_grad, LongTensor
import json

from flask import Flask, request

from io import BytesIO


def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

def get_property(request, property, default=None):
    value = request.args.get(property)
    return value if value is not None else default


cfg = json.loads(open('config.json').read())
model = cfg['model']
config = cfg['config']

hps_ms = utils.get_hparams_from_file(config)
n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys(
) else 0
n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
speakers = hps_ms.speakers if 'speakers' in hps_ms.keys() else ['0']
use_f0 = hps_ms.data.use_f0 if 'use_f0' in hps_ms.data.keys() else False
emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys(
) else False

net_g_ms = SynthesizerTrn(n_symbols,
                          hps_ms.data.filter_length // 2 + 1,
                          hps_ms.train.segment_size // hps_ms.data.hop_length,
                          n_speakers=n_speakers,
                          emotion_embedding=emotion_embedding,
                          **hps_ms.model).cuda()
_ = net_g_ms.eval()

utils.load_checkpoint(model, net_g_ms)

app = Flask(__name__)

@app.route('/tts')
def tts():
    speaker = int(get_property(request, 'speaker', '0').strip())
    text = get_property(request, 'text').strip()
    length_scale = float(get_property(request, 'length_scale', 1.1))
    noise_scale = float(get_property(request, 'noise_scale', 0.667))
    noise_scale_w = float(get_property(request, 'noise_scale_w', 0.8))

    stn_tst = get_text(text, hps_ms)
    with no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = LongTensor([stn_tst.size(0)]).cuda()
        sid = LongTensor([speaker]).cuda()  ## speaker id
        audio = net_g_ms.infer(
            x_tst,
            x_tst_lengths,
            sid=sid,
            noise_scale=noise_scale,
            noise_scale_w=noise_scale_w,
            length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()

    buffer = BytesIO()
    sf.write(buffer,
                audio,
                samplerate=hps_ms.data.sampling_rate,
                format='WAVEX')
    return buffer.getvalue(), 200, {"Content-Type": "audio/x-wav"}

@app.route("/list")
def list_speaker():
    return speakers


app.run(host='0.0.0.0')