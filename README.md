# MoeGoe Simple API Server

This is a simple API server for MoeGoe. For more information about MoeGoe, please see the [MoeGoe repository](https://github.com/CjangCjengh/MoeGoe).

## API Reference

### `GET /tts`

This endpoint generates a WAV file from the given text using the specified speaker and audio parameters.

#### Request

- Method: `GET`
- URL: `/tts`
- Query Parameters:
  - `text` (string, required): The text to generate audio from.
  - `speaker` (integer, optional, default: `0`): The ID of the speaker to use for generating audio.
  - `length_scale` (float, optional, default: `1.1`): The length scale factor to use for audio generation.
  - `noise_scale` (float, optional, default: `0.667`): The noise scale factor to use for audio generation.
  - `noise_scale_w` (float, optional, default: `0.8`): The noise scale w factor to use for audio generation.

#### Response

If the request is successful, the response will be a WAV file containing the generated audio. The audio will be in 16-bit PCM format, with a sample rate of 22050 Hz and a single channel (mono).

### `GET /info`

This endpoint returns server information.

#### Request

- Method: `GET`
- URL: `/info`

#### Response

If the request is successful, the response will be a JSON object in the following format:

```json
{
  "languages": ["zh", "en"],
  "speakers":[
  {
    "name": "Speaker A",
    "id": 0
  },
  {
    "name": "Speaker B",
    "id": 1
  },
  {
    "name": "Speaker C",
    "id": 2
  }
]
}
```

- `languages`: an array of language codes (strings) supported by the server. For example: `["zh", "en"]`.
- `speakers`: an array of objects representing available speakers. Each object has the following properties:
  - `name`: the name of the speaker (string).
  - `id`: the ID of the speaker (integer).
