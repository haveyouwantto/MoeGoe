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

### `GET /list`

This endpoint returns a list of available speakers.

#### Request

- Method: `GET`
- URL: `/list`

#### Response

If the request is successful, the response will be a JSON array containing a list of speakers in the following format:

```json
[
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
```

Each object in the array represents a single speaker and contains the following fields:
- `name` (string): the name of the speaker.
- `id` (integer): a unique identifier for the speaker.